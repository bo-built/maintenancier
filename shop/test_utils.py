from django.contrib.auth.models import User
from django.test import TestCase
from shop.models import (
    Shop,
    ShopUser,
    Machine,
    MaintenanceTask,
    LogEntry,
)


def generate_test_data():
    user = User.objects.create_user(
        username='dinaf@cloud9.com',
        password='supers@f32',
        first_name='Dina',
        last_name='Fox',
    )

    shop = Shop(name='Cloud 9 Ozark Highlands')
    shop.save()

    shop_user = ShopUser.objects.create(shop=shop, user=user)

    addtl_users = [
        ('glenns@cloud9.com', 'Glenn', 'Sturgis'),
        ('sandrak@cloud9.com', 'Sandra', 'Kaluiokalani'),
        ('mateol@cloud9.com', 'Mateo', 'Liwanag'),
    ]

    addtl_shop_users = []

    for _au in addtl_users:
        addtl_user = User.objects.create_user(
            username=_au[0],
            first_name=_au[1],
            last_name=_au[2],
            password='supers@f32',
        )
        addtl_shop_user = ShopUser.objects.create(shop=shop, user=addtl_user)
        addtl_shop_users.append(addtl_shop_user)

    machine_names = [
        'Cleaning Bot',
        'Box Crusher',
    ]
    machines = []

    for machine_name in machine_names:
        machine = Machine.objects.create(name=machine_name, shop=shop)
        machines.append(machine)

    maintenance_items = []
    _maintenance_items = [
        {
            'name': 'Charge cleaning bot',
            'interval': 1,
            'machine': machines[0],
        },
        {
            'name': 'Train cleaning bot on new walkways',
            'interval': 30,
            'machine': machines[0],
        },
        {
            'name': 'Change filters on cleaning bot',
            'interval': 7,
            'machine': machines[0],
        },
        {
            'name': 'Grease compactor gears',
            'interval': 14,
            'machine': machines[1],
        },
        {
            'name': 'Check for feet',
            'interval': 7,
            'machine': None,
        },
    ]

    log_items = []

    for mi in _maintenance_items:
        new_item = MaintenanceTask.objects.create(
            shop=shop,
            name=mi['name'],
            interval=mi['interval'],
            machine=mi['machine'],
        )
        maintenance_items.append(new_item)
        log_items.append(LogEntry.objects.get(task=new_item))

    return (
        user,
        shop,
        shop_user,
        machines,
        maintenance_items,
        log_items,
        addtl_shop_users,
    )


class PopulatedTestBase(TestCase):

    def setUp(self):
        (
            self.user,
            self.shop,
            self.shop_user,
            self.machines,
            self.maintenance_items,
            self.log_items,
            self.addtl_shop_users,
        ) = generate_test_data()
