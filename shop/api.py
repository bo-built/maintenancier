from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from shop.models import ShopUser, Machine, MaintenanceLogEntry

from shop import serializers


class AuthenticatedApiView(APIView):
    def get_permissions(self):
        return [IsAuthenticated()]


class ShopUserBaseApi(AuthenticatedApiView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if kwargs.get('shop_pk'):
            self.shopuser = get_object_or_404(
                ShopUser,
                user=request.user,
                shop__pk=kwargs['shop_pk']
            )

            self.shop = self.shopuser.shop


class ShopUserApi(ShopUserBaseApi):

    def get(self, request, shop_pk):
        url_path = request.resolver_match.url_name
        if url_path == 'shop_user_list_api':
            serializer = serializers.shopUserSerializer(self.shop.shopuser_set, many=True)
        else:
            serializer = serializers.shopUserSerializer(self.shopuser)
        return Response(serializer.data)

    def post(self, request, shop_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def patch(self, request, shop_pk, shop_user_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def delete(self, request, shop_pk, shop_user_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class ShopApi(ShopUserBaseApi):

    def get(self, request, shop_pk=None):
        if shop_pk:
            serializer = serializers.shopSerializer(self.shop)
        else:
            shops = [su.shop for su in request.user.shopuser_set.all()]
            serializer = serializers.shopSerializer(shops, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = serializers.shopSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    serializer.save()
                    shop_user = ShopUser(
                        user=request.user,
                        shop=serializer.instance
                    )
                    shop_user.save()
                    return Response(
                        {
                            'status': 'ok',
                            'message': 'Shop created',
                            'data': serializer.data
                        },
                        status=status.HTTP_201_CREATED,
                    )
            else:
                return Response(
                    {
                        'status': 'error',
                        'message': 'Data error',
                        'errors': serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except:  # noqa TO DO
            return Response(
                {
                    'status': 'error',
                    'message': 'Data error',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, shop_pk):
        try:
            serializer = serializers.shopSerializer(
                self.shop,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': 'ok',
                        'message': 'Shop updated',
                        'data': serializer.data,
                    },
                )
            else:
                return Response(
                    {
                        'status': 'error',
                        'message': 'Data error',
                        'errors': serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:  # noqa TO DO
            return Response(
                {
                    'status': 'error',
                    'message': 'Data error',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, shop_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class MachineApi(ShopUserBaseApi):
    def get(self, request, shop_pk):
        machines = self.shop.machine_set.all()
        serializer = serializers.machineSerializer(machines, many=True)
        return Response(serializer.data)

    def post(self, request, shop_pk):
        try:
            new_machine = Machine(shop=self.shop)
            serializer = serializers.machineSerializer(
                new_machine,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': 'ok',
                        'message': 'Machine created',
                        'machine': serializer.data,
                    },
                )
        except:  # noqa TO DO
            return Response(
                {
                    'status': 'error',
                    'message': 'Data error',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, shop_pk, machine_pk):
        try:
            serializer = serializers.machineSerializer(
                self.shop.machine_set.get(pk=machine_pk),
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': 'ok',
                        'message': 'Machine updated',
                        'data': serializer.data,
                    },
                )

            return Response(
                {
                    'status': 'error',
                    'message': 'Data error',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except:  # noqa TO DO
            return Response(
                {
                    'status': 'error',
                    'message': 'Data error',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, shop_pk, machine_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class MaintenanceScheduleApi(ShopUserBaseApi):
    def get(self, request, shop_pk, interval=None):
        if interval:
            if interval == 'today':
                instances = self.shop.get_upcoming_day()
            elif interval == 'week':
                instances = self.shop.get_upcoming_week()
            elif interval == 'month':
                instances = self.shop.get_upcoming_thirty_days_excluding_this_week()

            serializer = serializers.maintenanceLogEntrySerializer(instances, many=True)
            return Response(serializer.data)
        else:
            today = self.shop.get_upcoming_day()
            this_week = self.shop.get_upcoming_week()
            this_month = self.shop.get_upcoming_thirty_days_excluding_this_week()
            data = {
                'today': {
                    'title': 'Due Today',
                    'items': serializers.maintenanceLogEntrySerializer(today, many=True).data,
                },
                'this_week': {
                    'title': 'Upcoming Within a Week',
                    'items': serializers.maintenanceLogEntrySerializer(this_week, many=True).data,
                },
                'this_month': {
                    'title': 'Upcoming Within a Month',
                    'items': serializers.maintenanceLogEntrySerializer(this_month, many=True).data,
                },
            }
            return Response(data)

    def post(self, request, shop_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def patch(self, request, shop_pk, item_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def delete(self, request, shop_pk, item_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class MaintenanceLogEntryApi(ShopUserBaseApi):
    def get(self, request, shop_pk, item_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def post(self, request, shop_pk, item_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def patch(self, request, shop_pk, item_pk, log_item_pk):
        log_item = get_object_or_404(MaintenanceLogEntry, pk=log_item_pk)

        done_by_data = request.data.get('done_by')
        save_kwargs = {}

        if done_by_data is not None and request.data.get('status') == 'done':
            if isinstance(done_by_data, dict) and 'pk' in done_by_data:
                # Verify the ShopUser belongs to the same shop for security
                save_kwargs['done_by'] = get_object_or_404(
                    ShopUser,
                    pk=done_by_data['pk'],
                    shop__pk=shop_pk
                )
            else:
                save_kwargs['done_by'] = None
        if request.data.get('status') != 'done':
            save_kwargs['done_by'] = None
            save_kwargs['done_date'] = None

        serializer = serializers.maintenanceLogEntrySerializer(
            log_item,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save(**save_kwargs)
            return Response(
                {
                    'status': 'ok',
                    'message': 'Log item updated',
                    'log_item': serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                'status': 'error',
                'message': 'serializer errors',
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, shop_pk, item_pk, log_item_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
