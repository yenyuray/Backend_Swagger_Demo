from django.db import transaction
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView

from core.models import Order
from core.serializers import OrderSerializer


class OrdersView(GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **krgs):
        orders = self.get_queryset()
        serializer = self.serializer_class(orders, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
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
