from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

from shop.models import (
    Shop,
    ShopUser,
    Machine,
    MaintenanceScheduleItem,
    MaintenanceLogEntry,
)


local_test_data = {
    'shops': [
        {
            'name': 'Five x Five Studio',
            'machines': [
                {
                    'name': 'DeWalt Compact Tablesaw',
                    'maintenance_tasks': [
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
                    'maintenance_tasks': [
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
                    'maintenance_tasks': [
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
                    'maintenance_tasks': [
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
            'machines': [
                {
                    'name': 'SawStop - single blade',
                    'maintenance_tasks': [
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
                    'maintenance_tasks': [
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
                    'maintenance_tasks': [
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
                    'maintenance_tasks': [
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
                    'maintenance_tasks': [
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
                    'maintenance_tasks': [
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


def generate_local_test_data():
    today = timezone.now()
    Shop.objects.all().delete()
    Machine.objects.all().delete()
    MaintenanceScheduleItem.objects.all().delete()
    MaintenanceLogEntry.objects.all().delete()

    user = User.objects.get(pk=1)

    for _shop in local_test_data['shops']:
        shop = Shop.objects.create(name=_shop['name'])
        shopuser = ShopUser.objects.create(shop=shop, user=user)

        for _machine in _shop['machines']:
            machine = Machine.objects.create(shop=shop, name=_machine['name'])

            for _task in _machine['maintenance_tasks']:
                start_date = today + timedelta(days=_task['start_date_distance'])
                task = MaintenanceScheduleItem.objects.create(
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
                    log_item = MaintenanceLogEntry(
                        item=task,
                        done_by=shopuser,
                        done_date=done_date,
                        due_date=done_date,
                        status=MaintenanceLogEntry.Status.DONE,
                    )
                    log_item.save(bypass_child=True, force_done_date=True)
