from django.core.management.base import BaseCommand
from shop.utils.generate_test_data import TestData
from shop.utils.local_test_data import local_test_data


class Command(BaseCommand):
    help = 'Wipes all local users and shops and resets them with test data.'

    def handle(self, *args, **options):
        test_data = TestData(local_test_data)
        test_data.generate_local_test_data()
        print (
            "Local test data generated. You can login using:\n{}\n{}".format(
                test_data.test_data['user']['email'],
                test_data.test_data['user']['password']
            )
        )
