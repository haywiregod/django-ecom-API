import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from products.models import Status as ProductStatus
from cart.models import Cart
from orders.models import Order, Status
from orders.serializers import OrderSerializer, OrderReterieveSerializer
from rest_framework.response import Response
from faker import Faker
import razorpay
from django.shortcuts import render
from dotenv import load_dotenv
load_dotenv()

RZP_KEY_ID = os.environ.get("RZP_KEY_ID")
RZP_SECRET_KEY = os.environ.get("RZP_KEY")


def create_order(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user).all()
    if len(cart_items) <= 0:
        raise ValidationError({"message": "Cart is Empty"})
    total_amount = 0
    products = []
    is_product_active = ProductStatus.objects.filter(text="Active").first()
    non_active_products = []
    for item in cart_items:
        if (item.product.status == is_product_active):
            total_amount += item.product.price*item.quantity
            products.append(item.product)
        else:
            non_active_products.append(item.product)
    if(len(non_active_products) > 0):
        cart_items.filter(product__in=non_active_products).delete()

        raise ValidationError(
            {"message": f"{len(non_active_products)} Product(s) are not available anymore. They have been removed from the cart"})
    status = Status.objects.filter(text="Pending").first()
    order_id = Faker().bothify(text="O-#####-?????",
                               letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    order = Order.objects.create(
        user=user, status=status, final_amount=total_amount)
    for product in products:
        order.products.add(product)
    order.order_id = order_id
    order.save()
    return order


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_cod_order(request):
    order = create_order(request=request)
    order.status = Status.objects.filter(text="COD (Cash on Delivery)").first()
    order.save()
    # empty the cart
    Cart.objects.filter(user=request.user).delete()
    serializer = OrderSerializer(instance=order)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_rzp_order(request):
    order = create_order(request=request)
    client = razorpay.Client(
        auth=(RZP_KEY_ID, RZP_SECRET_KEY))
    data = {"amount": order.final_amount*100,
            "currency": "INR", "receipt": order.order_id}
    try:
        payment = client.order.create(data=data)
        order.rzp_order_id = payment['id']
        order.save()
    except Exception as e:
        print(e)
        return Response({'success': False, 'message': 'Something went wrong'}, 503)
    options = {
        "key": RZP_KEY_ID,
        "amount": order.final_amount*100,
        "currency": "INR",
        "name": "Acme Corp",
        "description": "Test Transaction",
        "image": "https://example.com/your_logo",
        "order_id": payment['id'],
        "prefill": {
            "name": request.user.name,
            "email": request.user.email,
            "contact": "9999999999"
        },
        "notes": {
            "address": "Razorpay Corporate Office"
        },
        "theme": {
            "color": "#3399cc"
        }
    }
    data = {
        "success": True,
        "order_id": order.order_id,
        "options": options
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_order_payment(request):
    client = razorpay.Client(
        auth=(RZP_KEY_ID, RZP_SECRET_KEY))
    required_keys = ['order_id', 'razorpay_payment_id', 'razorpay_signature']
    input_data_keys = request.data.keys()
    for required_key in required_keys:
        if required_key not in input_data_keys:
            msg = ", ".join(required_keys)
            raise ValidationError({"message": f"[{msg}] are required keys"})

    order_id = request.data['order_id']
    razorpay_payment_id = request.data['razorpay_payment_id']
    razorpay_signature = request.data['razorpay_signature']
    order = Order.objects.filter(
        order_id=order_id, user=request.user).first()
    if(order is None):
        print('hereere')
        msg = {
            "success": False,
            "message": f"Order not found for order ID {order_id}"
        }
        code = 400
        return Response(msg, code)
    razorpay_order_id = order.rzp_order_id

    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        status = Status.objects.filter(text="Pre-Paid").first()
        order.status = status
        order.payment_id = razorpay_payment_id
        order.rzp_signature = razorpay_signature
        order.save()
        # empty the cart
        Cart.objects.filter(user=request.user).delete()
        response_data = {
            "success": True,
            "message": "Payment Verified"
        }
        code = 201
    except Exception as e:

        response_data = {
            "success": False,
            "message": "Payment not Verified",
            "error": str(e)
        }
        code = 422
    return Response(response_data, code)


def payment_view(request):
    return render(request, "orders/payment.html")


class RetrieveOrderAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderReterieveSerializer

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        return orders
    lookup_field = 'order_id'
    lookup_url_kwarg = 'order_id'


class ListOrderAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderReterieveSerializer

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        return orders
    lookup_field = 'order_id'
    lookup_url_kwarg = 'order_id'
