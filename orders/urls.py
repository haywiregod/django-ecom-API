from django.urls import path
from orders.views import ListOrderAPIView, RetrieveOrderAPIView, create_cod_order, create_rzp_order, payment_view, verify_order_payment

urlpatterns = [
    path('', ListOrderAPIView.as_view()),
    path('payment', payment_view),
    path('cod', create_cod_order),
    path('pre-paid', create_rzp_order),
    path('verify-payment', verify_order_payment),
    path('<str:order_id>/', RetrieveOrderAPIView.as_view())
]
