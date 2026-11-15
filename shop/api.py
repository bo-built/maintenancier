from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from shop.models import ShopUser

from shop import serializers


class shopApi(APIView):
    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request):
        shops = [su.shop for su in request.user.shopuser_set.all()]
        serializer = serializers.shopSerializer(shops, many=True)
        return Response(serializer.data)

    def post(self, request):
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

        return Response(
            {
                'status': 'error',
                'message': 'Data error',
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        serializer = serializers.shopSerializer(data=request.data)
        if serializer.is_valid():
            # calling shop_user to get the shop ensures that the shop is
            # associated with the logged in user and so they are allowed
            # to change it
            shop_user = ShopUser.objects.get(
                user=request.user,
                shop__pk=pk
            )

            serializer = serializers.shopSerializer(
                shop_user.shop,
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

        return Response(
            {
                'status': 'error',
                'message': 'Data error',
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
