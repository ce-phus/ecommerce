from django.contrib import admin
from django.urls import path, include
from apps.order.views import admin_order_pdf
from apps.core.views import index
from apps.store.views import category_detail, product_detail, search
from apps.store.api import api_remove_from_cart, api_add_to_cart, create_checkout_session
from apps.cart.views import cart_detail, success
from apps.coupon.api import api_can_use
from apps.newsletter.api import api_add_subscriber
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.userprofile.views import signup, myaccount, logout
from apps.payment.views import initiate_payment, verify_payment

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('cart/', cart_detail, name='cart'),
    path('cart/success/', success, name='success'),
    path('admin/admin_order_pdf/<int:order_id>/', admin_order_pdf, name='admin_order_pdf'),
    path('', include('admin_material.urls')),
    path('admin/', admin.site.urls),

    # Auth
    path('myaccount/', myaccount, name='myaccount'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', logout, name='logout'),

    # API
    path('api/initiate_payment/', initiate_payment, name='initiate_payment'),
    path('api/verify_payment/<str:ref>/', verify_payment, name='verify_payment'),
    path('api/can_use/', api_can_use, name='api_can_use'),
    path('api/create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/add_subscriber/', api_add_subscriber, name='api_add_subscriber'),
    
    # Store
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('store/category/<slug:slug>/', category_detail, name='category_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'CGADGETS Computers Admin Portal'
