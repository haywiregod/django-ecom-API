import re
from django.http.response import Http404
from rest_framework.generics import (
    RetrieveAPIView, CreateAPIView,
    ListAPIView, ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, DestroyAPIView
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart
from .serializers import CartCreateSerailzer, CartUpdateReteriveDestroySerializer
from products.models import Product
# Create your views here.


class RetrieveUpdateDestroyCartAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartUpdateReteriveDestroySerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user)
        return cart

    def patch(self, request, pk):
        user = request.user
        cart_item = Cart.objects.filter(id=pk, user_id=user.id).first()
        if not cart_item:
            raise Http404
        data = {
            'user': user.id,
            'product': cart_item.product.id,
            'quantity': request.data['quantity']
        }
        serializer = CartUpdateReteriveDestroySerializer(
            instance=cart_item, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # def delete(self, request, pk):
    #     user = request.user


class AddToCartView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartCreateSerailzer

    def post(self, request, slug):
        product = Product.objects.filter(slug=slug).first()
        user = request.user
        data = {
            'user': user.id,
            'product': product.id
        }
        print(data)
        serializer = CartCreateSerailzer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # def delete(self, request, slug):
    #     product = Product.objects.filter(slug=slug).first()
    #     user = request.user
    #     request.data['product'] = product.id
    #     request.data['user'] = user.id
    #     serializer = CartUpdateReteriveDestroySerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.delete()
    #     return Response(serializer.data)


class CartRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartUpdateReteriveDestroySerializer

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user)
        return cart


class ListCartView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartUpdateReteriveDestroySerializer

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user)
        return cart
