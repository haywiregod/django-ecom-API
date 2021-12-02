from django.db import models

# Create your models here.


class Status(models.Model):
    text = models.CharField(max_length=128)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    slug = models.SlugField(max_length=128, unique=True)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name='status_text')
