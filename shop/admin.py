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


class MaintenanceTaskForm(forms.ModelForm):
    model = models.MaintenanceTask
    fields = '__all__'


@admin.register(models.MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    form = MaintenanceTaskForm


class LogEntryForm(forms.ModelForm):
    model = models.LogEntry
    fields = '__all__'


@admin.register(models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    form = LogEntryForm
    list_filter = ['status', 'done_date', 'due_date', 'task__shop']
