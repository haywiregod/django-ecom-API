from rest_framework import serializers
from .models import Product, Status


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class StatusSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Status
