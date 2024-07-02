from apps.cart.cart import Cart
import json

from django.conf import settings

from django.shortcuts import get_object_or_404
from apps.store.models import Product
from apps.order.models import Order
from apps.coupon.models import Coupon
from .utilities import decrement_product_quantity, send_order_confirmation
from django.http import JsonResponse
from apps.order.utils import checkout

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest

def create_checkout_session(request):
    data = json.loads(request.body)

    # Coupon
    coupon_code = data["coupon_code"]
    coupon_value = 0

    if coupon_code != '':
        coupon = Coupon.objects.get(code=coupon_code)

        if coupon.can_use():
            coupon_value = coupon_value
            coupon.use()
    
    cart = Cart(request)
    items = []
    
    for item in cart:
        product = item['product']

        price = int(product.price * 100)

        if coupon_value > 0:
            price = int(price * (int(coupon_value) / 100))

        obj = {
            'price_data': {
                'currency': 'ksh',
                'product_data': {
                    'name': product.title
                },
                'unit_amount': price
            },
            'quantity': item['quantity']
        }

        items.append(obj)

    gateway = data['gateway']
    session = ''
    order_id = ''
    payment_intent = ''

    # Create order

    orderid = checkout(request, data['first_name'], data['last_name'], data['email'], data['address'], data['zipcode'], data['place'], data['phone'])

    total_price = 0.00

    for item in cart:
        product = item['product']
        total_price = total_price + (float(product.price) * int(item['quantity']))

    if coupon_value > 0:
        total_price = total_price * (coupon_value / 100)

     # PayPal

    if gateway == 'paypal':
        order_id = data['order_id']
        environment = SandboxEnvironment(client_id=settings.PAYPAL_API_KEY_PUBLISHABLE, client_secret=settings.PAYPAL_API_KEY_HIDDEN)
        client = PayPalHttpClient(environment)

        request = OrdersCaptureRequest(order_id)
        response = client.execute(request)

        order = Order.objects.get(pk=orderid)
        order.paid_amount = total_price
        order.used_coupon = coupon_code

        if response.result.status == 'COMPLETED':
            order.paid = True
            order.payment_intent = order_id
            order.save()

            decrement_product_quantity(order)
            send_order_confirmation(order)
        else:
            order.paid = False
            order.save()
    else:
        order = Order.objects.get(pk=orderid)
        if gateway == 'razorpay':
            order.payment_intent = payment_intent['id']
        else:
            order.payment_intent = payment_intent
        order.paid_amount = total_price
        order.used_coupon = coupon_code
        order.save()

    #

    return JsonResponse({'session': session, 'order': payment_intent})

def api_add_to_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    cart = Cart(request)

    print("Product ID", data)
    product = get_object_or_404(Product, pk = product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)   
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)
    print("Added To cart")
    return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = str(data['product_id'])

    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse(jsonresponse)
