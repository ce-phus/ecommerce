from django.shortcuts import render
from .cart import Cart
import json
from django.conf import settings

def cart_detail(request):
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
            'thumbnail': product.get_thumbnail(),  # Call the method to get the URL
            'url': url,
            'num_available': product.num_available
        }
        products.append(product_data)

    productsstring = json.dumps(products)

    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        address = request.user.userprofile.address
        zipcode = request.user.userprofile.zipcode
        place = request.user.userprofile.place
        phone = request.user.userprofile.phone
    else:
        first_name = last_name = email = address = zipcode = place = phone = ''

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

    return render(request, 'cart/cart.html', context)

def success(request):
    cart = Cart(request)
    cart.clear()

    return render(request, 'cart/success.html')
