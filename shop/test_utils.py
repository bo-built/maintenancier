from django.contrib.auth.models import User
from shop.models import Shop, ShopUser, Machine, MaintenanceScheduleItem


def generate_test_data():
    user = User.objects.create_user(
        username='dinaf@cloud9.com',
        password='supers@f32',
    )

    shop = Shop(name='Cloud 9 Ozark Highlands')
    shop.save()

    shop_user = ShopUser(shop=shop, user=user)
    shop_user.save()

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

    for mi in _maintenance_items:
        new_item = MaintenanceScheduleItem.objects.create(
            shop=shop,
            name=mi['name'],
            interval=mi['interval'],
            machine=mi['machine'],
        )
        maintenance_items.append(new_item)

    return (
        user,
        shop,
        shop_user,
        machines,
        maintenance_items,
    )