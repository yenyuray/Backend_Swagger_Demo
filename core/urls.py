from django.urls import path, include
from .views import OrdersView

urlpatterns = [
    path('orders/', OrdersView.as_view())
]