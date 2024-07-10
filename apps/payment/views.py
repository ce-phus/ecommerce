from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Payment
from apps.order.models import Order, OrderItem

import json

from django.http import JsonResponse
from apps.cart.cart import Cart
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from apps.store.models import Product
from django.conf import settings
from django.contrib import messages
from apps.cart.cart import Cart
from apps.order.forms import OrderForm
from apps.payment.models import Payment


def verify_payment(request, ref):
    try:
        cart = Cart(request)
        payment = Payment.objects.get(ref=ref)
        verified = payment.verify_payment()

        if verified:
            # Fetch the correct order associated with the payment
            order = get_object_or_404(Order, id=payment.order_id)  # Assuming payment has an order_id field

            if order:
                order.paid = True  # Mark order as paid
                order.save()  # Save the order

                order_info = {
                    'id': order.id,
                    'total_cost': order.total_cost
                }

                context = {
                    'placed_order': order_info,
                    'payment': payment
                }

                cart.clear()  # Clear the cart after successful order
                return render(request, 'cart/success.html', context)
            else:
                messages.warning(request, 'Order not found')
                return JsonResponse({'error_message': 'Order not found'})
        else:
            messages.warning(request, 'Oops, your order was not processed. Please contact support.')
            return redirect('/')
    except Payment.DoesNotExist:
        messages.warning(request, 'Payment not found for this reference.')
        return JsonResponse({'error_message': 'Payment not found.'})
    
@login_required
def initiate_payment(request):
    cart = Cart(request)
    products = []

    for item in cart:
        product = item['product']
        url = f'/{product.category.slug}/{product.slug}/'
        product_data = {
            'id': product.id,
            'title': product.title,
            'price': str(product.price),
            'quantity': item['quantity'],
            'total_price': str(item['total_price']),
            'thumbnail': product.get_thumbnail(),
            'url': url,
            'num_available': product.num_available
        }
        products.append(product_data)

    productsstring = json.dumps(products)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            total_cost = 0
            order = form.save(commit=False)
            order.user = user

            for item in cart:
                product_in_cart = item['product']
                quantity_in_cart = item['quantity']
                product_instance = get_object_or_404(Product, pk=product_in_cart.id)

                order.total_cost += product_instance.price * quantity_in_cart
                order.save()

                OrderItem.objects.create(
                    order=order, 
                    product=product_instance, 
                    price=product_instance.price, 
                    quantity=quantity_in_cart
                )

            payment = Payment.objects.create(amount=order.total_cost, email=user.email, user=user)
            payment.save()

            context = {
                'cart': cart,
                'order': order,
                'total_cost': order.total_cost,
                'payment': payment,
                'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
                'productsstring': productsstring,
                'orderitem': ', '.join([item['title'] for item in products])
            }
            return render(request, 'cart/make_payment.html', context)
        else:
            form_errors = form.errors.as_text()
            messages.warning(request, f'Error: Invalid Data. Details: {form_errors}')
            return redirect('start_order')
    else:
        first_name = request.user.first_name if request.user.is_authenticated else ''
        last_name = request.user.last_name if request.user.is_authenticated else ''
        email = request.user.email if request.user.is_authenticated else ''
        address = request.user.userprofile.address if request.user.is_authenticated else ''
        zipcode = request.user.userprofile.zipcode if request.user.is_authenticated else ''
        place = request.user.userprofile.place if request.user.is_authenticated else ''
        phone = request.user.userprofile.phone if request.user.is_authenticated else ''

        context = {
            'cart': cart,
            'cart_total': len(cart),
            'productsstring': productsstring,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address,
            'zipcode': zipcode,
            'place': place,
            'pub_key_paypal': settings.PAYPAL_API_KEY_PUBLISHABLE
        }

        return render(request, 'cart/checkout.html', context)

