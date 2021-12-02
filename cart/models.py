from django.db import models
from django.db.models.deletion import DO_NOTHING
from products.models import Product
from users.models import User
# Create your models here.


class Cart(models.Model):
    product = models.ForeignKey(
        Product, related_name="product", on_delete=DO_NOTHING)
    user = models.ForeignKey(
        User, related_name="user", on_delete=DO_NOTHING)
    quantity = models.IntegerField(null=False, default=1)
