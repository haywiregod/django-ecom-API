from django.db.models import fields
from rest_framework import serializers
from rest_framework import validators
from rest_framework.validators import UniqueTogetherValidator

from products.serializers import ProductSerializer
from users.serializers import UserSerializer
from .models import Cart


class CartUpdateReteriveDestroySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
        depth = 2


class CartCreateSerailzer(CartUpdateReteriveDestroySerializer):
    user = None

    class Meta:
        model = Cart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=['user', 'product'],
                message="This Product has already been added to cart"
            )
        ]
        depth = 0
