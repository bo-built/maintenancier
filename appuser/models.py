from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_appuser(sender, instance, created, **kwargs):
    ''' Create a new AppUser instance and link it to a new User
    '''
    if created:
        AppUser.objects.create(user=instance)


@receiver(pre_save, sender=User)
def sync_username_to_email(sender, instance, **kwargs):
    ''' Set username to match email before saving to the database.
        Ensure that username is always saved in lowercase.
    '''
    if instance.email and instance.username != instance.email:
        instance.username = instance.email.strip().lower()

    if instance.username and not instance.email:
        instance.email = instance.username

    instance.username = instance.username.strip().lower()


class AppUser(models.Model):
    ''' Serves as an app specific profile model to connect Django User
        profiles to app user profiles and related models
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} // {}: {}'.format(
            self.user.username,
            self.user.pk,
            self.pk
        )
