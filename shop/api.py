from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from shop import services

from shop.models import (
    ShopUser,
    Machine,
    MaintenanceTask,
    LogEntry,
)

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
                shop = services.create_shop(
                    user=request.user,
                    validated_data=serializer.data
                )
                serializer = serializers.shopSerializer(shop)
                return Response(
                    {
                        'status': 'ok',
                        'message': 'Shop created',
                        'data': serializer.data,
                    },
                    status=status.HTTP_201_CREATED
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
                    'errors': 'Unknown Error',
                },
                status=status.HTTP_418_IM_A_TEAPOT
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
                    'errors': 'Unknown Error',
                },
                status=status.HTTP_418_IM_A_TEAPOT
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
    def get(self, request, shop_pk, machine_pk=None):
        if machine_pk:
            machine = get_object_or_404(
                self.shop.machine_set,
                pk=machine_pk
            )
            serializer = serializers.machineSerializer(machine)
        else:
            machines = self.shop.machine_set.filter(status='active').all()
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
                status=status.HTTP_418_IM_A_TEAPOT
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
                        'machine': serializer.data,
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
                status=status.HTTP_418_IM_A_TEAPOT
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
    def get(self, request, shop_pk, interval=None, machine_pk=None):
        url_path = request.resolver_match.url_name
        if url_path in ['maintenance_history_api', 'maintenance_machine_history_api']:
            if machine_pk:
                machine = get_object_or_404(
                    self.shop.machine_set,
                    pk=machine_pk
                )
                instances = self.shop.get_machine_maintenance_history(machine)
                serializer = serializers.LogEntrySerializer(instances, many=True)
            else:
                instances = self.shop.get_maintenance_history()
                serializer = serializers.LogEntrySerializer(instances, many=True)
            return Response(serializer.data)
        elif url_path == 'maintenance_schedule_by_interval_api':
            if interval == 'day':
                instances = self.shop.get_upcoming_day()
            elif interval == 'week':
                instances = self.shop.get_upcoming_week()
            elif interval == 'month':
                instances = self.shop.get_upcoming_thirty_days_excluding_this_week()
            # elif interval == 'history':
            #    instances = self.shop.get_maintenance_history()
            else:
                return Response(
                    {
                        'status': 'error',
                        'message': 'Bad request - interval options are "day", "week", "month"',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = serializers.LogEntrySerializer(instances, many=True)
            return Response(serializer.data)
        else:
            today = self.shop.get_upcoming_day()
            this_week = self.shop.get_upcoming_week()
            this_month = self.shop.get_upcoming_thirty_days_excluding_this_week()
            data = {
                'today': {
                    'title': 'Due Today',
                    'items': serializers.LogEntrySerializer(today, many=True).data,
                },
                'this_week': {
                    'title': 'Upcoming Within a Week',
                    'items': serializers.LogEntrySerializer(this_week, many=True).data,
                },
                'this_month': {
                    'title': 'Upcoming Within a Month',
                    'items': serializers.LogEntrySerializer(this_month, many=True).data,
                },
            }
            return Response(data)

    def post(self, request, shop_pk):
        try:
            new_item = MaintenanceTask(shop=self.shop)
            serializer = serializers.MaintenanceTaskSerializer(
                new_item,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': 'ok',
                        'message': 'Item created',
                        'item': serializer.data,
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
                    'errors': 'Unkown Error',
                },
                status=status.HTTP_418_IM_A_TEAPOT
            )

    def patch(self, request, shop_pk, task_pk):
        try:
            item = MaintenanceTask.objects.get(pk=task_pk)
            serializer = serializers.MaintenanceTaskSerializer(
                item,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                if request.data.get('next_due_date'):
                    next_due_date = date.fromisoformat(request.data['next_due_date'])
                    entry = item.next_scheduled
                    if entry is not None and entry.due_date != next_due_date:
                        entry.due_date = next_due_date
                        entry.save(update_fields=['due_date'])
                return Response(
                    {
                        'status': 'ok',
                        'message': 'Maintenance task updated',
                        'task': serializer.data,
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
                    'errors': 'Unkown Error',
                },
                status=status.HTTP_418_IM_A_TEAPOT
            )

    def delete(self, request, shop_pk, task_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class LogEntryApi(ShopUserBaseApi):
    def get(self, request, shop_pk, task_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def post(self, request, shop_pk, task_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def patch(self, request, shop_pk, task_pk, log_entry_pk):
        log_item = get_object_or_404(LogEntry, pk=log_entry_pk)

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

        serializer = serializers.LogEntrySerializer(
            log_item,
            data=request.data,
            partial=True,
        )

        try:
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
            else:
                return Response(
                    {
                        'status': 'error',
                        'message': 'serializer errors',
                        'errors': serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:  # noqa TO DO
            return Response(
                {
                    'status': 'error',
                    'message': 'Data error',
                    'errors': 'Unkown Error',
                },
                status=status.HTTP_418_IM_A_TEAPOT
            )

    def delete(self, request, shop_pk, task_pk, log_entry_pk):
        return Response(
            {
                'status': 'error',
                'message': 'This method is not implemented yet',
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
