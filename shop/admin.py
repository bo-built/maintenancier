from django.contrib import admin
from django import forms

from shop import models


class ShopForm(forms.ModelForm):
    model = models.Shop
    fields = '__all__'


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    form = ShopForm


class ShopUserForm(forms.ModelForm):
    model = models.ShopUser
    fields = '__all__'


@admin.register(models.ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    form = ShopUserForm


class MachineForm(forms.ModelForm):
    model = models.Machine
    fields = '__all__'


@admin.register(models.Machine)
class MachineAdmin(admin.ModelAdmin):
    form = MachineForm


class MaintenanceScheduleItemForm(forms.ModelForm):
    model = models.MaintenanceScheduleItem
    fields = '__all__'


@admin.register(models.MaintenanceScheduleItem)
class MaintenanceScheduleItemAdmin(admin.ModelAdmin):
    form = MaintenanceScheduleItemForm


class MaintenanceLogEntryForm(forms.ModelForm):
    model = models.MaintenanceLogEntry
    fields = '__all__'


@admin.register(models.MaintenanceLogEntry)
class MaintenanceLogEntryAdmin(admin.ModelAdmin):
    form = MaintenanceLogEntryForm
    list_filter = ['status', 'done_date', 'due_date', 'item__shop']
