from django.db import models
from django.utils import timezone


class Order(models.Model):
    order_id = models.AutoField(auto_created=True, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now())
    last_update_date = models.DateTimeField(auto_now=True)
    list_of_items = models.TextField(max_length=1000)
