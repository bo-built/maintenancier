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

local_test_data = {
    'other_users': [
        {
            'first_name': 'Dina',
            'last_name': 'Fox',
            'email': 'dfox@test.com'
        },
        {
            'first_name': 'Sandra',
            'last_name': 'Kaluiokalani',
            'email': 'sandra@mailg.com'
        },
        {
            'first_name': 'Glenn',
            'last_name': 'Sturgis',
            'email': 'glenn@sturgisandsons.com'
        },
    ],
    'shops': [
        {
            'name': 'Five x Five Studio',
            'general_maintenance': [
                {
                    'name': 'Sweep Floors',
                    'interval': 1,
                    'description': '''Sweep floors around machines.''',
                    'start_date_distance': 0,
                },
                {
                    'name': 'Organize cutoffs',
                    'interval': 7,
                    'description': '''Organize cutoffs and scrap ones that won't be used.''',
                    'start_date_distance': 0,
                },
            ],
            'machines': [
                {
                    'name': 'DeWalt Compact Tablesaw',
                    'tasks': [
                        {
                            'name': 'Clean & Inspect Blades',
                            'interval': 7,
                            'description': '''Use PitchRx and nylon brush to clean blades.
                                Inspect blades for any chips or cracks.''',
                            'start_date_distance': 3,
                        },
                    ],
                },
                {
                    'name': 'Laguna Dust Collector',
                    'tasks': [
                        {
                            'name': 'Empty Dust Bag',
                            'interval': 1,
                            'description': 'If dust bag is 3/4 or more full, empty it.',
                            'start_date_distance': 0,
                        },
                        {
                            'name': 'Clean Baffle',
                            'interval': 14,
                            'description': '''Remove filter from baffle casing
                                and clean with air gun.''',
                            'start_date_distance': 7,
                        },
                    ],
                },
                {
                    'name': 'Chisel Set',
                    'tasks': [
                        {
                            'name': 'Sharpen',
                            'interval': 14,
                            'description': 'Check all chisels and sharpen as needed',
                            'start_date_distance': 5,
                        },
                    ],
                },
                {
                    'name': 'Rikon Bandsaw',
                    'tasks': [
                        {
                            'name': 'Clean cabinet',
                            'interval': 30,
                            'description': '''Open the cabinet and vaccuum sawdust, grease
                                wheel bearings if needed''',
                            'start_date_distance': 0,
                        },
                    ],
                },
            ]
        },
        {
            'name': 'The Sawdust Shack',
            'general_maintenance': [
                {
                    'name': 'Sweep Floors',
                    'interval': 1,
                    'description': '''Sweep floors around machines, especially in walkways.''',
                    'start_date_distance': 0,
                },
                {
                    'name': 'Dumpster run',
                    'interval': 7,
                    'description': '''Take trash cart and recycle bins to dumpsters.''',
                    'start_date_distance': 0,
                },
                {
                    'name': 'Organize lumber racks',
                    'interval': 30,
                    'description': '''Go through lumber ans scrap cutoffs that won't be used,
                    organize sheetgoods cutoffs.''',
                    'start_date_distance': 0,
                },
            ],
            'machines': [
                {
                    'name': 'SawStop - single blade',
                    'tasks': [
                        {
                            'name': 'Clean & Inspect Blades',
                            'interval': 7,
                            'description': '''Use PitchRx and nylon brush to clean blades.
                                Inspect blades for any chips or cracks.''',
                            'start_date_distance': 3,
                        },
                        {
                            'name': 'Clean cabinet',
                            'interval': 30,
                            'description': '''Open up cabinet and vaccuum sawdust, inspect dust port
                                for clogs, check if any bearings need grease''',
                            'start_date_distance': 1,
                        },
                        {
                            'name': 'Align fence',
                            'interval': 14,
                            'description': 'Verify fence alignment to blade',
                            'start_date_distance': 1,
                        },
                        {
                            'name': 'Clean tabletop',
                            'interval': 60,
                            'description': 'Use metal cleanser to wipe down top',
                            'start_date_distance': 0,
                        },
                    ],
                },
                {
                    'name': 'SawStop - dado stack',
                    'tasks': [
                        {
                            'name': 'Clean & Inspect Blades',
                            'interval': 7,
                            'description': '''Use PitchRx and nylon brush to clean blades.
                                Inspect blades for any chips or cracks.''',
                            'start_date_distance': 4,
                        },
                        {
                            'name': 'Clean cabinet',
                            'interval': 30,
                            'description': '''Open up cabinet and vaccuum sawdust, inspect dust port
                                for clogs, check if any bearings need grease''',
                            'start_date_distance': 5,
                        },
                        {
                            'name': 'Align fence',
                            'interval': 14,
                            'description': 'Verify fence alignment to blade',
                            'start_date_distance': 7,
                        },
                        {
                            'name': 'Clean tabletop',
                            'interval': 60,
                            'description': 'Use metal cleanser to wipe down top',
                            'start_date_distance': 1,
                        },
                    ],
                },
                {
                    'name': 'Planer - Grizzly 12"',
                    'tasks': [
                        {
                            'name': 'Rotate and check blades',
                            'interval': 60,
                            'description': '''For each knife blade on the helical blade head,
                                rotate 90d clockwise and check for chips. If blades have already
                                been rotated 3 times, replace them.''',
                            'start_date_distance': 2,
                        },
                        {
                            'name': 'Grease Blade Bearings',
                            'interval': 30,
                            'description': '''Using red machine lubricant and grease gun,
                                grease the left and right bearings''',
                            'start_date_distance': 6,
                        },
                    ],
                },
                {
                    'name': 'Jointer - Jet 8"',
                    'tasks': [
                        {
                            'name': 'Rotate and check blades',
                            'interval': 60,
                            'description': '''For each knife blade on the helical blade head,
                                rotate 90d clockwise and check for chips. If blades have already
                                been rotated 3 times, replace them.''',
                            'start_date_distance': 8,
                        },
                        {
                            'name': 'Check fence alignment',
                            'interval': 14,
                            'description': 'Check and adjust the fence alignment as needed',
                            'start_date_distance': 9,
                        },
                    ],
                },
                {
                    'name': 'Powermatic Dust Cyclone (Jointers & Planers)',
                    'tasks': [
                        {
                            'name': 'Check duct system for clogs',
                            'interval': 30,
                            'description': '',
                            'start_date_distance': 4,
                        },
                        {
                            'name': 'Empty Dust bags',
                            'interval': 1,
                            'description': 'If bags are 3/4 or more full, empty them.',
                            'start_date_distance': 0,
                        },
                        {
                            'name': 'Clean Baffle',
                            'interval': 14,
                            'description': '''Remove filter from baffle casing
                                and clean with air gun.''',
                            'start_date_distance': 7,
                        },
                    ],
                },
                {
                    'name': 'Jet Dust Collector (SawStops)',
                    'tasks': [
                        {
                            'name': 'Clean Baffle',
                            'interval': 14,
                            'description': '''Remove filter from baffle casing
                                and clean with air gun.''',
                            'start_date_distance': 7,
                        },
                        {
                            'name': 'Empty Dust bags',
                            'interval': 1,
                            'description': 'If bags are 3/4 or more full, empty them.',
                            'start_date_distance': 0,
                        },
                    ],
                },
            ]
        },
    ]
}


def generate_task(_task, shop, shopuser, machine, users):
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
    past_iteration_cap = 90
    past_iterations = round(past_iteration_cap / _task['interval'])
    for i in range(past_iterations):
        days_ago = (i + 1) * _task['interval']
        done_date = start_date - timedelta(days=days_ago)
        print("i: {}, interval: {}, days ago: {}, done: {}".format(
                i,
                _task['interval'],
                days_ago,
                done_date
            )
        )
        log_entry = LogEntry(
            task=task,
            done_by=random.choice(users),
            done_date=done_date,
            due_date=done_date,
            status=LogEntry.Status.DONE,
        )
        log_entry.save(bypass_child=True, force_done_date=True)


def generate_shop_user(_user, shop):
    user = User.objects.filter(email=_user['email']).first()
    if not user:
        user = User.objects.create(
            first_name=_user['first_name'],
            last_name=_user['last_name'],
            email=_user['email'],
        )
    shop_user = ShopUser.objects.create(shop=shop, user=user)
    return shop_user


def generate_local_test_data():
    Shop.objects.all().delete()
    Machine.objects.all().delete()
    MaintenanceTask.objects.all().delete()
    LogEntry.objects.all().delete()

    user = User.objects.get(pk=1)

    for _shop in local_test_data['shops']:
        shop = Shop.objects.create(name=_shop['name'])
        shopuser = ShopUser.objects.create(shop=shop, user=user)
        users = [shopuser, ]
        for other_user in local_test_data['other_users']:
            users.append(generate_shop_user(other_user, shop))

        shop_standin = shop.machine_set.get(is_shop=True)

        for shop_maintenance in _shop['general_maintenance']:
            generate_task(shop_maintenance, shop, shopuser, shop_standin, users)

        for _machine in _shop['machines']:
            machine = Machine.objects.create(shop=shop, name=_machine['name'])

            for _task in _machine['tasks']:
                generate_task(_task, shop, shopuser, machine, users)
