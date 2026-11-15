from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ApiRegisterViewTest(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='glenns@cloud9.com',
            email='glenns@cloud9.com',
            password='supers@f32here',
        )

    async def test_successful_api_register(self):
        ''' Verify that a POST call to the user registration API endpoint with
            expected and correct data is successful
        '''
        url = reverse('appuser:api-profile')
        payload = {
            'first_name': 'Dina',
            'last_name': 'Fox',
            'email': 'dinaf@cloud9.com',
            'password': 'p@rr0Ts123'
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'User profile registered')
        verified_user_object = await User.objects.aget(
            username=payload['email'])

        self.assertEqual(verified_user_object.email, payload['email'])
        self.assertEqual(verified_user_object.username, payload['email'])
        self.assertEqual(
            verified_user_object.first_name,
            payload['first_name']
        )
        self.assertEqual(verified_user_object.last_name, payload['last_name'])

    async def test_attempted_duplicate_username_api_register(self):
        ''' Verify that a POST call to the user registration API endpoint with
            a duplicate username is handled appropriately
        '''
        url = reverse('appuser:api-profile')
        payload = {
            'first_name': 'Glenn',
            'last_name': 'Sturgis',
            'email': 'glenns@cloud9.com',
            'password': 'supers@f32here'
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['message'],
            'This email address is already in use'
        )