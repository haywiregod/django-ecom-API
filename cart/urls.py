from django.urls import path

from .views import AddToCartView, ListCartView, RetrieveUpdateDestroyCartAPIView

urlpatterns = [
    path("", ListCartView.as_view()),
    path("<int:pk>", RetrieveUpdateDestroyCartAPIView.as_view()),
    path("<slug:slug>", AddToCartView.as_view())

]
