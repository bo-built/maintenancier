from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    name = models.CharField(max_length=250, unique=True)


class ShopUser(models.Model):
    ''' Links a User to a shop
        Users can have multiple shops and shops can have multiple users
    '''
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Machine(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    class meta:
        unique_together = ['shop', 'name', ]


class MaintenanceScheduleItem(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
