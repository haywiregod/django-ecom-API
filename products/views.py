from rest_framework import serializers
from rest_framework import pagination
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from products.serializers import ProductSerializer
from .models import Product, Status
# Create your views here.


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductAPIView(ListCreateAPIView):
    queryset = Product.objects.filter(
        status=Status.objects.filter().first()).select_related().order_by('-id')

    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    # return Response(serialized_products.data)
