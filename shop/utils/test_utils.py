from django.contrib.auth.models import User
from django.test import TestCase

from shop.utils.generate_test_data import TestData
from shop.utils.local_test_data import local_test_data

class PopulatedTestBase(TestCase):

    def setUp(self):
        test_data = TestData(local_test_data)
        test_data.generate_local_test_data()
        self.user = test_data.main_user
        self.shop = test_data.shops[1]
        self.shop_user = self.shop.shopuser_set.select_related('user').get(user=self.user)
        self.machines = self.shop.machine_set.all()
        self.maintenance_items = []
        self.log_items = []
        for machine in self.machines:
            for task in machine.maintenance_items.all():
                self.maintenance_items.append(task)
                for log_entry in task.log_entries.all():
                    self.log_items.append(log_entry)

        self.addtl_shop_users = list(
            self.shop.shopuser_set.select_related('user').exclude(user=self.user)
        )
