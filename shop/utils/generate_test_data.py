import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

from shop.models import (
    Shop,
    ShopUser,
    Machine,
    MaintenanceTask,
    LogEntry,
)


class TestData():
    """ Class for generating test data. This can be used IRL by calling
        `python manage.py generate_local_test_data`

        It is also used for most test cases, using
        shop.utils.test_utils.PopulatedTestBase()
    """
    BACKFILL_DAYS = 90

    def __init__(self, test_data):
        self.test_data = test_data
        self.main_user = None
        self.shops = []

    def generate_task_and_log_entries(self, _task, shop, machine, users):
        """ Creates a task with given data for given shop and machine.

            Goes back BACKFILL_DAYS days and populates completed log entries of
            the task and assigns it to a random user from users.
        """
        today = timezone.now()
        start_date = today + timedelta(days=_task['start_date_distance'])
        task = MaintenanceTask.objects.create(
            shop=shop,
            machine=machine,
            name=_task['name'],
            description=_task['description'],
            interval=_task['interval'],
            start_date=start_date,
        )
        done_date = start_date
        past_iteration_cap = self.BACKFILL_DAYS
        past_iterations = round(past_iteration_cap / _task['interval'])
        for i in range(past_iterations):
            days_ago = (i + 1) * _task['interval']
            done_date = start_date - timedelta(days=days_ago)
            # print("i: {}, interval: {}, days ago: {}, done: {}".format(
            #         i,
            #         _task['interval'],
            #         days_ago,
            #         done_date
            #     )
            # )
            log_entry = LogEntry(
                task=task,
                done_by=random.choice(users),
                done_date=done_date,
                due_date=done_date,
                status=LogEntry.Status.DONE,
            )
            log_entry.save(bypass_child=True, force_done_date=True)
        return task


    def generate_main_user(self):
        main_user = User.objects.create_user(
            first_name=self.test_data['user']['first_name'],
            last_name=self.test_data['user']['last_name'],
            username=self.test_data['user']['email'],
            email=self.test_data['user']['email'],
            password=self.test_data['user']['password'],
        )
        return main_user


    def generate_shop_user(self, _user, shop):
        user = User.objects.filter(email=_user['email']).first()
        if not user:
            user = User.objects.create_user(
                first_name=_user['first_name'],
                last_name=_user['last_name'],
                email=_user['email'],
                username=_user['email'],
                password='supers@f32',
            )
        shop_user = ShopUser.objects.create(shop=shop, user=user)
        return shop_user


    def generate_shop_data(self, _shop):
        shop = Shop.objects.create(name=_shop['name'])
        shopuser = ShopUser.objects.create(shop=shop, user=self.main_user)
        users = [shopuser, ]
        for other_user in _shop['other_users']:
            users.append(self.generate_shop_user(other_user, shop))

        shop_standin = shop.machine_set.get(is_shop=True)

        for shop_maintenance in _shop['general_maintenance']:
            self.generate_task_and_log_entries(shop_maintenance, shop, shop_standin, users)

        for _machine in _shop['machines']:
            machine = Machine.objects.create(shop=shop, name=_machine['name'])

            for _task in _machine['tasks']:
                self.generate_task_and_log_entries(_task, shop, machine, users)
        return shop


    def generate_local_test_data(self):
        User.objects.all().delete()
        Shop.objects.all().delete()
        Machine.objects.all().delete()
        MaintenanceTask.objects.all().delete()
        LogEntry.objects.all().delete()

        self.main_user = self.generate_main_user()

        for _shop in self.test_data['shops']:
            self.shops.append(self.generate_shop_data(_shop,))
