from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


class StatusModel(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ARCHIVED = 'archived', 'Archived'

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Track the initial status loaded from the DB (None for unsaved new objects)
        self._original_status = self.status if self.pk else None

    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default='active',
        db_index=True,
    )


class Shop(models.Model):
    ''' Main object for the app - representes a physical shop or org that
        requires routine maintenance that needs to be scheduled and logged
    '''
    def __str__(self):
        return 'Shop <pk: {}> -- {}'.format(self.pk, self.name)

    name = models.CharField(max_length=250, unique=True)

    @property
    def shop_dashboard_url(self):
        return reverse('shop:shop_dashboard', kwargs={'shop_pk': self.pk})

    @property
    def shop_api_url(self):
        return reverse('shopapi:shop_detail_api', kwargs={'shop_pk': self.pk})

    @property
    def machine_api_url(self):
        return reverse('shopapi:machine_api', kwargs={'shop_pk': self.pk})

    @property
    def schedule_api_url(self):
        return reverse('shopapi:maintenance_schedule_api', kwargs={'shop_pk': self.pk})

    @property
    def shopuser_list_api_url(self):
        return reverse('shopapi:shop_user_list_api', kwargs={'shop_pk': self.pk})

    @property
    def shopuser_api_url(self):
        return reverse('shopapi:shop_user_api', kwargs={'shop_pk': self.pk})

    def get_upcoming_day(self):
        today = timezone.localdate()
        overdue = LogEntry.objects.filter(
            task__shop=self,
            due_date__lte=today,
            status__in=['overdue', 'pending'],
            task__status='active',
        )

        due_today = LogEntry.objects.filter(
            task__shop=self,
            due_date=today,
            status__in=['overdue', 'pending'],
            task__status='active',
        )

        done_today = LogEntry.objects.filter(
            task__shop=self,
            due_date__lte=today,
            done_date__date=today,
            status='done',
            task__status='active',
        )

        result = overdue.union(due_today, done_today).order_by('due_date').all()

        return result

        '''
        TO DO : Figure out this single query. Until then, brute force it
        return LogEntry.objects.filter(
            # get todays items
            Q(due_date=today)
            # get old items that aren't done yet
            | Q(due_date__lte=today, status__in=['overdue', 'pending'])
            # get old items that were done today
            | Q(due_date__lte=today, done_date=today),
            task__shop=self,
        )
        '''

    def get_upcoming_week(self):
        '''
        '''
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)
        week_end = tomorrow + timedelta(days=6)
        return LogEntry.objects.filter(
            task__shop=self,
            due_date__gte=tomorrow,
            due_date__lte=week_end,
            task__interval__gt=1,
            task__status='active',
        ).exclude(status='dismissed').order_by('due_date').all()

    def get_upcoming_thirty_days_excluding_this_week(self):
        today = timezone.localdate()
        week_end = today + timedelta(days=6)
        month_end = week_end + timedelta(days=30)
        return LogEntry.objects.filter(
            task__shop=self,
            due_date__gt=week_end,
            due_date__lte=month_end,
            task__interval__gt=1,
            task__status='active',
        ).exclude(status='dismissed').order_by('due_date').all()

    def get_maintenance_history(self):
        return LogEntry.objects.filter(
            task__shop=self,
            status='done',
        ).order_by('-done_date').all()

    def get_machine_maintenance_history(self, machine):
        return LogEntry.objects.filter(
            task__shop=self,
            task__machine=machine,
            status='done',
        ).order_by('-done_date').all()


class ShopUser(StatusModel):
    ''' Links a User to a shop
        Users can have multiple shops and shops can have multiple users
    '''
    def __str__(self):
        return 'Shop User <pk: {}> -- {} // {}'.format(
            self.pk,
            self.user.username,
            self.shop
        )

    @classmethod
    def get_user_shops(cls, user):
        return [su.shop for su in cls.objects.filter(user=user)]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [('shop', 'user'), ]

    @property
    def name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    @property
    def api_url(self):
        return reverse(
            'shopapi:shop_user_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'shop_user_pk': self.pk,
            }
        )


class Machine(StatusModel):
    ''' Represents physical tool or machine that belongs to a shop.
        If is_shop is True, the instance represents the actual shop. This
        allows maintenance tasks to be created for the general shop that are
        not tied to a specific machine.

        It may or may not require maintenance log items.
    '''
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    is_shop = models.BooleanField(default=False)

    def __str__(self):
        return 'Machine <pk: {}> -- {} // {}'.format(
            self.pk,
            self.name,
            self.shop
        )

    class meta:
        unique_together = ['shop', 'name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Track the initial status loaded from the DB (None for unsaved new objects)
        self._original_status = self.status if self.pk else None

    def save(self, *args, **kwargs):
        ''' If an item is archived, delete incomplete future iterations
        '''
        just_archived = (
            self._original_status != self.Status.ARCHIVED
            and self.status == self.Status.ARCHIVED
        )

        super().save(*args, **kwargs)
        self._original_status = self.status

        if just_archived:
            for maintenance_task in self.maintenance_items.all():
                maintenance_task.status = 'archived'
                maintenance_task.save()

    @property
    def api_url(self):
        return reverse(
            'shopapi:machine_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'machine_pk': self.pk,
            }
        )

    @property
    def dashboard_url(self):
        return reverse(
            'shop:machine_dashboard',
            kwargs={
                'shop_pk': self.shop.pk,
                'machine_pk': self.pk,
            }
        )

    @property
    def maintenance_history_api(self):
        return reverse(
            'shopapi:maintenance_machine_history_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'machine_pk': self.pk,
            }
        )

    @property
    def shop_schedule_api_url(self):
        return reverse('shopapi:maintenance_schedule_api', kwargs={'shop_pk': self.shop.pk})


class MaintenanceTask(StatusModel):
    ''' Represents a maintenance task that needs to be scheduled and repeated
        at a regular interval. It can belong to a specific machine or to the
        shop in general.

        If item is for a specific machine, link it
        if it is not for a specific machine, leave it blank and we can
        assume it is a general shop item.

        If a machine is deleted, do not CASCADE - shop managers should decide
        via UX if a deleted machine should have its maintenance schedule removed
        entirely from the record or if the log should be kept.
    '''
    INTERVAL_CHOICES = [
        (1, 'Daily'),
        (7, 'Weekly'),
        (14, 'Every 2 weeks'),
        (30, 'Monthly'),
        (60, 'Every 2 months'),
        (90, 'Every 3 months'),
        (120, 'Every 6 months'),
        (365, 'Annually'),
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    machine = models.ForeignKey(
        Machine,
        null=True,
        related_name='maintenance_items',
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    interval = models.IntegerField(choices=INTERVAL_CHOICES, default=1)
    start_date = models.DateField(default=timezone.localdate)

    def __str__(self):
        if self.machine:
            display_name = self.machine.name
        else:
            display_name = 'Shop'
        return 'Maintenance Item <pk: {}> -- {}: {} // {} ({})'.format(
            self.pk,
            display_name,
            self.name,
            self.shop,
            self.get_interval_display(),
        )

    def save(self, *args, **kwargs):
        ''' If an item is archived, delete incomplete future iterations
        '''
        just_archived = (
            self._original_status != self.Status.ARCHIVED
            and self.status == self.Status.ARCHIVED
        )

        super().save(*args, **kwargs)
        self._original_status = self.status

        if just_archived:
            self.delete_incomplete_log_items()

    @property
    def display_interval(self):
        return self.get_interval_display()

    @property
    def api_url(self):
        return reverse(
            'shopapi:maintenance_schedule_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'task_pk': self.pk,
            }
        )

    @property
    def source(self):
        if self.machine:
            return self.machine.name
        return 'Shop'

    @property
    def next_scheduled(self):
        return self.log_entries.filter(
            status='pending',
        ).order_by('due_date').first()

    def delete_incomplete_log_items(self):
        self.log_entries.exclude(status='done').delete()


class LogEntry(models.Model):
    ''' Represents an instance of a maintenance schedule item being performed.

        It is performed by a user on a specific date and time.

        If an associated machine or user is deleted, do not CASCADE - shop managers
        should decide via UX if a deleted machine or user should have their maintenance
        log removed entirely from the record or if the log should be kept.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Track the initial status loaded from the DB (None for unsaved new objects)
        self._original_status = self.status if self.pk else None

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        DONE = 'done', 'Done'
        OVERDUE = 'overdue', 'Overdue'
        DISMISSED = 'dismissed', 'Dismissed'

    # source is the previous iteration that this task was generated from, if
    # it is not the first instance of a task's log entries
    source = models.ForeignKey(
        'LogEntry',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    task = models.ForeignKey(
        MaintenanceTask,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='log_entries',
    )
    due_date = models.DateField(default=timezone.localdate, db_index=True)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    done_by = models.ForeignKey(ShopUser, blank=True, null=True, on_delete=models.SET_NULL)
    done_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    _task_name = models.CharField(max_length=300, blank=True, null=True)
    _machine_name = models.CharField(max_length=300, blank=True, null=True)
    _description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Maintenance Log Entry <pk: {}> -- {} @ {} // {}'.format(
            self.pk,
            self.item_name,
            self.due_date,
            self.task.shop
        )

    def save(self, bypass_child=False, force_done_date=False, *args, **kwargs):
        ''' If an item is completed or dismissed, the next log item needs to be
            scheduled or updated.

            Create or update a child item and set its due date to item.interval
            days from today.
        '''
        just_completed = (
            self._original_status != self.Status.DONE
            and self.status == self.Status.DONE
        )
        just_dismissed = (
            self._original_status != self.Status.DISMISSED
            and self.status == self.Status.DISMISSED
        )

        generate_child = just_completed or just_dismissed

        if generate_child:
            today = timezone.now()
            if not force_done_date:
                self.done_date = today
            self._description = self.task.description
            self._task_name = self.task.name
            due_next = today + timedelta(days=self.task.interval)
            if self.task.machine:
                self._machine_name = self.task.machine.name

            if not bypass_child:
                child = LogEntry.objects.filter(source=self).first()
                if child:
                    child.due_date = due_next
                    child.save()
                else:
                    child = LogEntry(
                        source=self,
                        task=self.task,
                        due_date=due_next,
                        status=self.Status.PENDING,
                    )
                    child.save()

        super().save(*args, **kwargs)

        self._original_status = self.status

    @classmethod
    def from_db(cls, db, field_names, values):
        ''' IRL this would be done by a background task
            For now, just check log items as they are pulled
        '''
        instance = super().from_db(db, field_names, values)
        today = timezone.localdate()
        if instance.status == 'pending':
            if instance.due_date and instance.due_date < today:
                instance.status = 'overdue'
                instance.save()
        return instance

    @property
    def interval(self):
        return self.task.get_interval_display()

    @property
    def task_name(self):
        return self._task_name or self.task.name

    @property
    def machine_name(self):
        return self._machine_name or self.task.machine.name

    @property
    def machine_pk(self):
        if self.task.machine:
            return self.task.machine.pk
        return None

    @property
    def description(self):
        return self._description or self.task.description

    @property
    def api_url(self):
        return reverse(
            'shopapi:log_item_detail_api',
            kwargs={
                'shop_pk': self.task.shop.pk,
                'task_pk': self.task.pk,
                'log_entry_pk': self.pk,
            }
        )


@receiver(post_save, sender=MaintenanceTask)
def create_first_log_instance(sender, instance, created, **kwargs):
    ''' When a new maintenance item is created, initiate a schedule for it
    '''
    if created:
        if not instance.start_date:
            next_due = timezone.localdate() + timedelta(days=instance.interval)
        else:
            next_due = instance.start_date
        next_entry = LogEntry(
            task=instance,
            due_date=next_due,
        )
        next_entry.save()


@receiver(post_save, sender=Shop)
def create_general_shop_machine(sender, instance, created, **kwargs):
    ''' When a new shop is created, initiate a "general shop" machine
    '''
    if created:
        Machine.objects.create(
            shop=instance,
            name='General Shop',
            is_shop=True,
        )
