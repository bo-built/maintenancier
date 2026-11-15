from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from appuser.forms import (
    changePasswordForm,
    LoginForm,
    RegistrationForm,
    UserProfileForm,
)
from appuser.models import AppUser


class ProtectedView(LoginRequiredMixin, TemplateView):
    ''' Mixin for pages that require an authenticated user
    '''
    template_name = 'protected_dashboard.html'
    login_url = '/login/'


class UserProfileLandingPage(ProtectedView):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('appuser/user_profile.html')
        context = {
            'appuser': request.user.appuser,
            'form': UserProfileForm(),
            'password_change_form': changePasswordForm(),
        }
        return HttpResponse(template.render(context, request))


class Logout(ProtectedView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('appuser:login'))


class Login(View):
    ''' Render the login HTML page
    '''
    def get(self, request, *args, **kwargs):
        template = loader.get_template('appuser/authenticate.html')
        context = {
            'login_form': LoginForm,
            'registeration_form': RegistrationForm,
        }
        return HttpResponse(template.render(context, request))
