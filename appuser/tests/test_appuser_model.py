from django.contrib.auth.models import User
from django.test import TestCase
from appuser.models import AppUser


class AppUserModelTest(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='glenns@cloud9.com',
            email='glenns@cloud9.com',
            password='supers@f32here',
        )

    def test_appuser_created_when_user_saved(self):
        '''
            Verify that an AppUser instance is created when a User is created
            and that they are linked
        '''
        new_user = User(
            username='dinaf',
            email='dinaf@cloud9.com'
        )

        new_user.save()

        self.assertTrue(AppUser.objects.get(user=new_user))

    def test_username_syncs_to_email(self):
        ''' Verify that when a User email is updated the username syncs to it
            and that username is saved in all lowercase
        '''

        test_email_address = 'DinaF@cloud9.com'

        self.existing_user.email = test_email_address
        self.existing_user.save()

        self.assertEqual(
            self.existing_user.username,
            test_email_address.lower(),
        )
        self.assertEqual(
            self.existing_user.email,
            test_email_address,
        )
