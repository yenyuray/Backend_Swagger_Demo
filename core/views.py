from abc import ABC

from rest_framework import viewsets
from rest_framework.pagination import BasePagination

from core.models import Order
from core.serializers import OrderSerializer


class UnknownPagination(BasePagination, ABC):
    paginator_query_args = ['unknown_paginator']


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = UnknownPagination
