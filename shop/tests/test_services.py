from shop.utils.test_utils import PopulatedTestBase
from shop import services


class TestShopCreationServices(PopulatedTestBase):
    def test_shop_created_generates_shop_user(self):
        user = self.user
        data = {
            'name': 'The Sawdust Shack',
        }

        shop_obj = services.create_shop(
            user=user,
            validated_data=data,
        )

        shop_user = shop_obj.shopuser_set.get(user=self.user)
        self.assertIsNotNone(shop_user)
