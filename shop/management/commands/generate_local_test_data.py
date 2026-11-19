from django.core.management.base import BaseCommand
from shop.local_test_data import generate_local_test_data


class Command(BaseCommand):
    help = 'Wipes all local shops and resets them with test data.'

    def handle(self, *args, **options):
        generate_local_test_data()
