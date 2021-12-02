from django.db.models import fields
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Order, Status


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderReterieveSerializer(OrderSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        depth = 2
