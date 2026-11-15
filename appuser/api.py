import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from appuser import utils
from appuser import serializers


class LoginApi(APIView):
    ''' Handler for login requests via API
    '''
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.data['email'].lower(),
                password=serializer.data['password']
            )

            if user is not None:
                login(request, user)
                return JsonResponse(
                    {
                        'status': 'success',
                        'redirect_url': reverse('appuser:user_profile'),
                        'message': 'Successful log in',
                    }
                )

            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid username or password'
                },
                status=401
            )
        else:
            return Response(
                {
                    'status': 'error',
                    'message': 'Data error',
                    'errors': serializer.errors,
                },
                status=400
            )


class updatePasswordApi(APIView):
    def get_permissions(self):
        return [IsAuthenticated()]

    def post(self, request):
        provided_password_is_correct = request.user.check_password(
            request.data['current_password'])
        if not provided_password_is_correct:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Provided password not authenticated'
                },
                status=401
            )
        if not request.data['new_password'] == request.data['confirm_new_password']:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Passwords do not match'
                },
                status=401
            )

        password_is_valid, password_errors = utils.validate_password_strength(
            request.data['new_password'])

        if not password_is_valid:
            return Response(
                {
                    'status': 'error',
                    'message': 'Password has errors',
                    'errors': password_errors,
                },
                status=400,
            )
        try:
            request.user.set_password(request.data['new_password'])
            request.user.save()
            return JsonResponse(
                {
                    'status': 'ok',
                    'message': 'Password updated'
                }
            )
        except: # noqa TO DO
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid request'
                },
                status=400
            )


class ProfileApi(APIView):
    ''' Handler for profile update requests via API
    '''
    def get_permissions(self):
        ''' Allow POST (create) requests to be unauthenticated '''
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        serializer = serializers.ProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid JSON data'
                },
                status=400
            )

        email_is_changed = data['email'].lower().strip() != request.user.email.lower().strip()
        email_is_valid = email_is_changed and utils.email_is_unique(
            data['email']
        )

        if email_is_changed and not email_is_valid:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'This email address is already in use'
                },
                status=401
            )

        serializer = serializers.ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': 'ok',
                    'message': 'User profile updated',
                    'user': serializer.data,
                },
            )

        return Response(
            {
                'status': 'error',
                'message': 'Data error',
                'errors': serializer.errors,
            },
            status=400
        )

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid JSON data'
                },
                status=400
            )

        if not utils.email_is_unique(data['email']):
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'This email address is already in use'
                },
                status=401
            )

        serializer = serializers.ProfileSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            password_is_valid, password_errors = utils.validate_password_strength(
                request.data['password']
            )
            if password_is_valid:
                serializer.save()
                serializer.instance.set_password(request.data['password'])
                serializer.instance.save()

                return Response(
                    {
                        'status': 'ok',
                        'message': 'User profile registered',
                        'user': serializer.data,
                        'redirect_url': reverse('appuser:user_profile'),
                    },
                )
            else:
                return Response(
                    {
                        'status': 'error',
                        'message': 'Password has errors',
                        'errors': password_errors,
                        'user': serializer.data,
                        'redirect_url': reverse('appuser:user_profile'),
                    },
                    status=400,
                )

        return Response(
            {
                'status': 'error',
                'message': 'Data error',
                'errors': serializer.errors,
            },
            status=400
        )
