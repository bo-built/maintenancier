from django.db import transaction
from shop.models import Shop, ShopUser, LogEntry


@transaction.atomic
def create_shop(*, user, validated_data) -> Shop:
    """
    Creates a Shop and attaches the creating user as a ShopUser.
    """
    shop = Shop.objects.create(**validated_data)
    ShopUser.objects.create(user=user, shop=shop)
    return shop


@transaction.atomic
def update_log_entry(*, log_entry, validated_data) -> LogEntry:
    pass