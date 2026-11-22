from django.db import transaction
from django.shortcuts import get_object_or_404
from shop.models import Shop, ShopUser, Machine


@transaction.atomic
def create_shop(*, user, validated_data) -> Shop:
    """
    Creates a Shop and attaches the creating user as a ShopUser.
    It then creates a 'general shop' machine instance.
    """
    shop = Shop.objects.create(**validated_data)
    ShopUser.objects.create(user=user, shop=shop)
    Machine.objects.create(
        shop=shop,
        name='General Shop',
        is_shop=True,
    )
    return shop


def sanitize_log_entry_data(*, shop, request_data) -> dict:
    """ Configure the done by fields if they are present and return an
        updatable dictionary for saving a log_entry against a serializer
    """
    done_by_data = request_data.get('done_by')
    sanitized_data = {}

    if done_by_data is not None and request_data.get('status') == 'done':
        if isinstance(done_by_data, dict) and 'pk' in done_by_data:
            # Verify the ShopUser belongs to the same shop for security
            sanitized_data['done_by'] = get_object_or_404(
                ShopUser,
                pk=done_by_data['pk'],
                shop=shop
            )
        else:
            sanitized_data['done_by'] = None

    if request_data.get('status') != 'done':
        sanitized_data['done_by'] = None
        sanitized_data['done_date'] = None

    return sanitized_data
