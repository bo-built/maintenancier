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
        self.async_client.force_login(self.existing_user)

    async def test_provided_password_incorrect(self):
        ''' Verify that a POST call to the user registration API endpoint with
            expected and correct data is successful
        '''
        url = reverse('appuser:api-update-password')
        payload = {
            'current_password': 'supers@f32hereasdf',
            'new_password': 'p@rroTs123',
            'confirm_new_password': 'p@rroTs123',
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['message'], 'Provided password not authenticated')

    async def test_provided_passwords_dont_match(self):
        ''' Verify that a POST call to the user registration API endpoint with
            expected and correct data is successful
        '''
        url = reverse('appuser:api-update-password')
        payload = {
            'current_password': 'supers@f32here',
            'new_password': 'p@rroTs123',
            'confirm_new_password': 'p@rroTs123asdf',
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['message'], 'Passwords do not match')

    async def test_successful_update_password(self):
        ''' Verify that a POST call to the user registration API endpoint with
            expected and correct data is successful
        '''
        url = reverse('appuser:api-update-password')
        payload = {
            'current_password': 'supers@f32here',
            'new_password': 'p@rroTs123',
            'confirm_new_password': 'p@rroTs123',
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Password updated')
        password_updated = self.existing_user.check_password("p@rroTs123")

