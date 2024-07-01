from .cart import Cart

def cart_total(request):
    cart = Cart(request)
    return {'cart_total': len(cart)}
