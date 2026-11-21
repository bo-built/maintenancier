local_test_data = {
    'user': {
        'first_name': 'Jo',
        'last_name': 'Cooluser',
        'email': 'jo@test.com',
        'password': 'p@ssword123',
    },
    'shops': [
        {
            'name': 'Five x Five Studio',
            'other_users': [
                {
                    'first_name': 'Amy',
                    'last_name': 'Madison',
                    'email': 'amym@test.com'
                },
                {
                    'first_name': 'Jonathan',
                    'last_name': 'levinson',
                    'email': 'jonl@mailg.com'
                },
            ],
            'general_maintenance': [
                {
                    'name': 'Sweep Floors',
                    'interval': 1,
                    'description': 'Sweep floors around machines.',
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
                            'description': 'Use PitchRx and nylon brush to clean blades. Inspect blades for any chips or cracks.',
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
                            'description': 'Remove filter from baffle casing and clean with air gun.',
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
                            'description': 'Open the cabinet and vaccuum sawdust, grease wheel bearings if needed',
                            'start_date_distance': 0,
                        },
                    ],
                },
            ]
        },
        {
            'name': 'Cloud 9 Fabrication',
            'other_users': [
                {
                    'first_name': 'Dina',
                    'last_name': 'Fox',
                    'email': 'dina@cloud9fabrication.com'
                },
                {
                    'first_name': 'Sandra',
                    'last_name': 'Kaluiokalani',
                    'email': 'sandra@cloud9fabrication.com'
                },
                {
                    'first_name': 'Glenn',
                    'last_name': 'Sturgis',
                    'email': 'glenn@cloud9fabrication.com'
                },
            ],
            'general_maintenance': [
                {
                    'name': 'Dumpster run',
                    'interval': 7,
                    'description': 'Take trash cart and recycle bins to dumpsters.',
                    'start_date_distance': 0,
                },
                {
                    'name': 'Organize lumber racks',
                    'interval': 30,
                    'description': '''Go through lumber ans scrap cutoffs that won't be used, organize sheetgoods cutoffs.''',
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
                            'description': 'Use PitchRx and nylon brush to clean blades. Inspect blades for any chips or cracks.',
                            'start_date_distance': 3,
                        },
                        {
                            'name': 'Clean cabinet',
                            'interval': 30,
                            'description': 'Open up cabinet and vaccuum sawdust, inspect dust port for clogs, check if any bearings need grease',
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
                            'description': 'Use PitchRx and nylon brush to clean blades. Inspect blades for any chips or cracks.',
                            'start_date_distance': 4,
                        },
                        {
                            'name': 'Clean cabinet',
                            'interval': 30,
                            'description': 'Open up cabinet and vaccuum sawdust, inspect dust port for clogs, check if any bearings need grease',
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
                            'description': 'For each knife blade on the helical blade head, rotate 90d clockwise and check for chips. If blades have already been rotated 3 times, replace them.',
                            'start_date_distance': 2,
                        },
                        {
                            'name': 'Grease Blade Bearings',
                            'interval': 30,
                            'description': 'Using red machine lubricant and grease gun, grease the left and right bearings',
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
                            'description': 'For each knife blade on the helical blade head, rotate 90d clockwise and check for chips. If blades have already been rotated 3 times, replace them.',
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
                            'description': 'Remove filter from baffle casing and clean with air gun.',
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
                            'description': 'Remove filter from baffle casing and clean with air gun.',
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
                {
                    'name': 'Laguna CNC',
                    'tasks': [
                        {
                            'name': 'Grease Bearings',
                            'interval': 1,
                            'description': 'Use the grease gun and red tacky grease to inject grease into the X, Y amd Z axis bearings. Wipe clean after. Check if we need to order more grease.',
                            'start_date_distance': 1,
                        },
                        {
                            'name': 'Clean guide rails and lead screws',
                            'interval': 1,
                            'description': 'Use a dry cotton cloth to wipe dust from guide rails and lead screws daily after use. Use compressed air gun on gentle setting to clean away dust around bearings.',
                            'start_date_distance': 0,
                        },
                    ],
                },
                {
                    'name': 'Becker Vacuum Pump',
                    'tasks': [
                        {
                            'name': 'Clean Filters',
                            'interval': 30,
                            'description': '''Open the front filter cover and remove the filter. Dust it out using the compressed air gun. If you can't see light through it after dusting, replace it and order a new backup filter''',
                            'start_date_distance': 22,
                        },
                        {
                            'name': 'Check fan blades',
                            'interval': 1,
                            'description': 'Open the cover on the fan housing and remove each fan blade, noting the direction they are placed. Wipe them clean with a cotton rag. Use calipers to check their thickness - if it is less than 3mm, replace them. Put gloves on first.',
                            'start_date_distance': 0,
                        },
                    ],
                },
            ]
        },
    ]
}