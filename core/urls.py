from django.urls import path

from core.views import OrdersViewSet

order_list = OrdersViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
order_detail = OrdersViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('orders/', order_list, name='order-list'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),

]