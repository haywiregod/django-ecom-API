from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('users.urls')),
    path('api/v1/product/', include('products.urls')),
    path('api/v1/cart/', include('cart.urls')),
    path('api/v1/order/', include('orders.urls')),
]
