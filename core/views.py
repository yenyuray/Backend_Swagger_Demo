from django.db import transaction
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import BasePagination

from core.models import Order
from core.serializers import OrderSerializer


class UnknownPagination(BasePagination):
    paginator_query_args = ['unknown_paginator']


class OrdersView(GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_summary='Get Orders',
        operation_description='Get all orders',
        tags=['Orders']
    )
    def get(self, request):
        orders = self.get_queryset()
        serializer = self.serializer_class(orders, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    @swagger_auto_schema(
        operation_summary='Add new order ',
        operation_description='Add new order with item',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'list_of_items': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='List of items in order'
                )
            }
        ),
        tags=['Orders']
    )
    def post(self, request):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)


class OrderDetailSet(viewsets.ModelViewSet):
    model = Order
    queryset = Order.objects
    serializer_class = OrderSerializer
    pagination_class = UnknownPagination


# @swagger_auto_schema(
#     method='put',
#     manual_parameters=[
#         openapi.Parameter('test', openapi.IN_FORM, "test manual param", type=openapi.TYPE_STRING),
#     ],
#     request_body=OrderSerializer,
#     tags=['Order']
# )
# @swagger_auto_schema(methods=['get'], responses={
#     200: openapi.Response('response description', OrderSerializer),
# }, tags=['Order'])
# @api_view(['GET', 'PUT'])
# def order_detail(request, pk):
#     """user_detail fbv docstring"""
#     order = get_object_or_404(Order.objects, pk=pk)
#     serializer = OrderSerializer(order)
#     return Response(serializer.data)
