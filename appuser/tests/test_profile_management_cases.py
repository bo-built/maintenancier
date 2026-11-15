from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ApiUpdateProfileViewTest(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='glenns@cloud9.com',
            email='glenns@cloud9.com',
            password='sup3rs@f3',
            first_name='Glenn',
            last_name='Sturgis'
        )
        self.test_user = User.objects.create_user(
            username='sandrak@cloud9.com',
            email='sandrak@cloud9.com',
            password='thisisapassword',
            first_name='Sandra',
            last_name='Kaluiokalani'
        )
        self.async_client.force_login(self.test_user)

    async def test_successful_api_profile_update(self):
        ''' Verify that a POST call to the user profile update API endpoint
            with expected and correct data is successful
        '''
        url = reverse('appuser:api-profile')
        payload = {
            'first_name': 'Carol',
            'last_name': 'Malloon',
            'email': 'carolm@cloud9.com',
        }

        response = await self.async_client.patch(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'User profile updated')
        verified_user_object = await User.objects.aget(
            username=payload['email'])

        self.assertEqual(verified_user_object.email, payload['email'])
        self.assertEqual(verified_user_object.username, payload['email'])
        self.assertEqual(
            verified_user_object.first_name,
            payload['first_name']
        )
        self.assertEqual(verified_user_object.last_name, payload['last_name'])

    async def test_successful_api_profile_update_name_only(self):
        ''' Verify that a POST call to the user profile update API endpoint
            that is not updating the email address is successful

            This makes sure that the duplicate email check does not raise an
            error against the user's own email address
        '''
        url = reverse('appuser:api-profile')
        payload = {
            'first_name': 'Carol',
            'last_name': 'Malloon',
            'email': 'sandrak2@cloud9.com',
        }

        response = await self.async_client.patch(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'User profile updated')
        verified_user_object = await User.objects.aget(
            username=payload['email'])

        self.assertEqual(verified_user_object.email, payload['email'])
        self.assertEqual(verified_user_object.username, payload['email'])
        self.assertEqual(
            verified_user_object.first_name,
            payload['first_name']
        )
        self.assertEqual(verified_user_object.last_name, payload['last_name'])

    async def test_duplicate_email_api_profile_update(self):
        ''' Verify that a POST call to the user profile update API endpoint
            with a duplicate email address is hanfled appropriately
        '''
        url = reverse('appuser:api-profile')
        payload = {
            'first_name': 'Sandra',
            'last_name': 'Kaluiokalani',
            'email': 'glenns@cloud9.com',
        }

        response = await self.async_client.patch(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['message'],
            'This email address is already in use'
        )
