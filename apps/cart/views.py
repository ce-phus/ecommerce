from django.shortcuts import render
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    productsstring = ''

    for item in cart:
        product = item['product']
        url = '/%s/%s/' % (product.category.slug, product.slug)
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'url': '%s', 'num_available': '%s'}," % (product.id, product.title, product.price, item['quantity'], item['total_price'], product.get_thumbnail, url, product.num_available)

        productsstring = productsstring + b

    # if request.user.is_authenticated:
    #     pass
    # else:
    #     pass

    # context = {
    #     'cart': cart,
    #     'first_name': first_name,
    #     'last_name': last_name,
    #     'email': email,
    #     'phone': phone,
    #     'address': address,
    #     'zipcode': zipcode,
    #     'place': place,
    # }
        
        return render(request, 'cart/cart.html')
