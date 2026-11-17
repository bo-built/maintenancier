from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Shop(models.Model):
    ''' Main object for the app - representes a physical shop or org that
        requires routine maintenance that needs to be scheduled and logged
    '''
    def __str__(self):
        return 'Shop <pk: {}> -- {}'.format(self.pk, self.name)

    name = models.CharField(max_length=250, unique=True)

    def get_upcoming_day(self):
        return MaintenanceLogEntry.objects.filter(
            due_date__lte=date.today(),
            item__shop=self
        ).all()

    def get_upcoming_week(self):
        tomorrow = date.today() + timedelta(days=1)
        week_end = tomorrow + timedelta(days=6)
        return MaintenanceLogEntry.objects.filter(
            due_date__gte=tomorrow,
            due_date__lte=week_end,
            item__shop=self,
            item__interval__gt=1,
        ).all()

    def get_upcoming_thirty_days_excluding_this_week(self):
        week_end = date.today() + timedelta(days=6)
        month_end = week_end + timedelta(days=30)
        return MaintenanceLogEntry.objects.filter(
            due_date__gt=week_end,
            due_date__lte=month_end,
            item__shop=self,
            item__interval__gt=1,
        ).all()


class ShopUser(models.Model):
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
    is_selected = models.BooleanField(default=False, db_index=True)


class Machine(models.Model):
    ''' Represents physical tool or machine that belongs to a shop.

        It may or may not require maintenance log items.
    '''
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return 'Machine <pk: {}> -- {} // {}'.format(
            self.pk,
            self.name,
            self.shop
        )

    class meta:
        unique_together = ['shop', 'name', ]


class MaintenanceScheduleItem(models.Model):
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
        (1, 'daily'),
        (7, 'weekly'),
        (14, 'every 2 weeks'),
        (30, 'monthly'),
        (60, 'every 2 months'),
        (90, 'every 3 months'),
        (120, 'every 6 months'),
        (365, 'annually'),
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    machine = models.ForeignKey(
        Machine,
        blank=True,
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

    @property
    def source(self):
        if self.machine:
            return self.machine.name
        return 'Shop'


class MaintenanceLogEntry(models.Model):
    ''' Represents an instance of a maintenance schedule item being performed.

        It is performed by a user on a specific date and time.

        If an associated machine or user is deleted, do not CASCADE - shop managers
        should decide via UX if a deleted machine or user should have their maintenance
        log removed entirely from the record or if the log should be kept.
    '''
    item = models.ForeignKey(
        MaintenanceScheduleItem,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    due_date = models.DateField(default=timezone.localdate, db_index=True)
    status = models.CharField(
        max_length=15,
        default='to do',
        choices=[
            ('to do', 'to do'),
            ('done', 'done'),
            ('overdue', 'overdue'),
        ],
        db_index=True,
    )
    done_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    done_date = models.DateTimeField(auto_now_add=True)
    done_by_name = models.CharField(max_length=300, blank=True, null=True)
    _item_name = models.CharField(max_length=300, blank=True, null=True)
    _machine_name = models.CharField(max_length=300, blank=True, null=True)
    _description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Maintenance Log Entry <pk: {}> -- {} @ {} // {}'.format(
            self.pk,
            self.item_name,
            self.due_date,
            self.item.shop
        )

    @property
    def interval(self):
        return self.item.get_interval_display()

    @property
    def item_name(self):
        return self._item_name or self.item.name

    @property
    def machine_name(self):
        return self._machine_name or self.item.machine.name

    @property
    def description(self):
        return self._description or self.item.description


@receiver(post_save, sender=MaintenanceScheduleItem)
def create_first_log_instance(sender, instance, created, **kwargs):
    ''' When a new maintenance item is created, initiate a schedule for it
    '''
    if created:
        next_due = instance.start_date + timedelta(days=instance.interval)
        next_entry = MaintenanceLogEntry(
            item=instance,
            due_date=next_due,
        )
        next_entry.save()
