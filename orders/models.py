from django.db import models
from django.db.models.deletion import DO_NOTHING
from products.models import Product
from users.models import User
# Create your models here.


class Status(models.Model):
    text = models.CharField(max_length=128)


class Order(models.Model):
    order_id = models.CharField(max_length=128)
    user = models.ForeignKey(
        User, related_name='by_user', on_delete=DO_NOTHING)
    products = models.ManyToManyField(
        Product, related_name="products")
    status = models.ForeignKey(
        Status, related_name="status", on_delete=DO_NOTHING)
    final_amount = models.FloatField(null=False)
    payment_id = models.TextField(null=True)
    rzp_order_id = models.CharField(max_length=255, null=True)
    rzp_signature = models.TextField(null=True)
