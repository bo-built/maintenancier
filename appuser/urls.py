from django.urls import path
from appuser import api as appuser_api_views
from appuser import views as appuser_views

app_name = 'appuser'

urlpatterns = [
    path(
        'login/',
        appuser_views.Login.as_view(),
        name='login',
    ),
    path(
        'logout/',
        appuser_views.Logout.as_view(),
        name='logout',
    ),
    path(
        'profile/',
        appuser_views.UserProfileLandingPage.as_view(),
        name='user_profile',
    ),
    path(
        'api/authenticate-login/',
        appuser_api_views.LoginApi.as_view(),
        name='api-authenticate-login',
    ),
    path(
        'api/profile/',
        appuser_api_views.ProfileApi.as_view(),
        name='api-profile',
    ),
    path(
        'api/update-password/',
        appuser_api_views.updatePasswordApi.as_view(),
        name='api-update-password',
    ),
]