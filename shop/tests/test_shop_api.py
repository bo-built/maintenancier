from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shop.models import Shop, ShopUser


class ApiShopPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='dinaf@cloud9.com',
            password='supers@f32',
        )
        self.async_client.force_login(self.user)

    async def test_successful_shop_creation(self):
        ''' Verify new shop instance is created from successful post call
        '''
        url = reverse('shop:shop_api')

        payload = {
            'name': 'Cloud 9 Ozark Highlands',
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'Shop created')


class ApiShopPatchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='dinaf@cloud9.com',
            password='supers@f32',
        )
        self.async_client.force_login(self.user)

        self.shop = Shop(name='Cloud 9 Ozark Highlands')
        self.shop.save()

        self.shop_user = ShopUser(shop=self.shop, user=self.user)
        self.shop_user.save()

    async def test_successful_shop_update(self):
        ''' Verify new shop instance is created from successful post call
        '''

        new_shop_name = 'Cloud 9 Ozark Highlands Distribution Center'

        url = reverse('shop:shop_detail_api', kwargs={'pk': self.shop.pk})

        payload = {
            'name': new_shop_name,
        }

        response = await self.async_client.patch(
            url,
            data=payload,
            content_type='application/json',
        )

        await self.shop.arefresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Shop updated')
        self.assertEqual(self.shop.name, new_shop_name)
