from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse


class ApiLoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='dinaf@cloud9.com',
            password='supers@f32',
        )

    async def test_successful_api_login(self):
        ''' Verify a vanilla successful POST to the login API endpoint
        '''
        url = reverse('appuser:api-authenticate-login')

        payload = {
            'email': 'dinaf@cloud9.com',
            'password': 'supers@f32'
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Successful log in')

    async def test_successful_api_login_case_insensitive_username(self):
        ''' Verify a successful POST to the login API
            endpoint is case insensitive
        '''
        url = reverse('appuser:api-authenticate-login')

        payload = {
            'email': 'DinaF@cloud9.com',
            'password': 'supers@f32'
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Successful log in')

    async def test_bad_password(self):
        ''' Verify that a POST call to the login API endpoint with an
            incorrect password is handled appropriately
        '''
        url = reverse('appuser:api-authenticate-login')

        payload = {
            'email': 'dinaf@cloud9.com',
            'password': 'supers@f32FFF'
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['message'],
            'Invalid username or password'
        )

    async def test_bad_username(self):
        ''' Verify that a POST call to the login API endpoint with a
            nonexistant username is handled appropriately
        '''
        url = reverse('appuser:api-authenticate-login')

        payload = {
            'email': 'glens@cloud9.com',
            'password': 'supers@f32FFF'
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['message'],
            'Invalid username or password'
        )