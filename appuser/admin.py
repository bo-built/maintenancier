from django.contrib import admin
from django import forms

from appuser.models import AppUser


class AppUserForm(forms.ModelForm):
    model = AppUser
    fields = '__all__'


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    form = AppUserForm
