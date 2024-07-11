import json
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from apps.store.models import Product
from apps.order.models import Order
from apps.coupon.models import Coupon
from apps.cart.cart import Cart
from .utilities import decrement_product_quantity, send_order_confirmation
from apps.order.utils import checkout
from paypalhttp import HttpError
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest

def create_checkout_session(request):
    data = json.loads(request.body)

    # Coupon
    coupon_code = data.get("coupon_code", "")
    coupon_value = 0

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.can_use():
                coupon_value = coupon.value
                coupon.use()
        except Coupon.DoesNotExist:
            pass

    cart = Cart(request)
    items = []

    for item in cart:
        product = item['product']
        price = int(product.price * 100)

        if coupon_value > 0:
            price = int(price * (1 - (coupon_value / 100)))

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

    total_price = sum(float(item['product'].price) * item['quantity'] for item in cart)
    if coupon_value > 0:
        total_price = total_price * (1 - (coupon_value / 100))

    # PayPal
    if gateway == 'paypal':
        order_id = data['order_id']
        environment = SandboxEnvironment(client_id=settings.PAYPAL_API_KEY_PUBLISHABLE, client_secret=settings.PAYPAL_API_KEY_HIDDEN)
        client = PayPalHttpClient(environment)

        order = Order.objects.get(pk=orderid)

        # Check if the order has already been paid
        if order.paid:
            return JsonResponse({'error': 'Order already paid'}, status=400)

        request = OrdersCaptureRequest(order_id)
        try:
            response = client.execute(request)
            if response.result.status == 'COMPLETED':
                order.paid = True
                order.paid_amount = total_price
                order.used_coupon = coupon_code
                order.payment_intent = order_id
                order.save()

                decrement_product_quantity(order)
                send_order_confirmation(order)
            else:
                order.paid = False
                order.save()
        except HttpError as err:
            error_details = err.status_code, err.headers, err.message
            print(f"PayPal API error: {error_details}")
            if err.status_code == 422 and "ORDER_ALREADY_CAPTURED" in err.message:
                order.paid = True
                order.paid_amount = total_price
                order.used_coupon = coupon_code
                order.payment_intent = order_id
                order.save()

                decrement_product_quantity(order)
                send_order_confirmation(order)
            else:
                return JsonResponse({'error': 'Payment capture failed'}, status=400)

    return JsonResponse({'session': session, 'order': payment_intent})

def api_add_to_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    cart = Cart(request)

    print("Product ID", data)
    product = get_object_or_404(Product, pk=product_id)

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
