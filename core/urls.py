from django.urls import path

from core import views
from .views import OrderDetailSet

order_detail = OrderDetailSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('orders/', views.OrdersView.as_view()),
    path('orders/<int:pk>/', order_detail)

]