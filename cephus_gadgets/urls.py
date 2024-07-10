"""
URL configuration for cephus_gadgets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.core.views import index
from django.conf import settings
from django.conf.urls.static import static
from apps.store.views import category_detail, product_detail, search
from apps.store.api import api_remove_from_cart, api_add_to_cart, create_checkout_session
from apps.cart.views import cart_detail, success
from apps.coupon.api import api_can_use
from apps.newsletter.api import api_add_subscriber
from django.contrib.auth import views
from apps.userprofile.views import signup, myaccount, logout
from apps.payment.views import initiate_payment, verify_payment
from apps.order.views import admin_order_pdf





urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('cart/', cart_detail, name='cart'),
    path('success/', success, name='success'),
    path('admin/', admin.site.urls),
    path('admin/admin_order_pdf/<int:order_id>/', admin_order_pdf, name='admin_order_pdf'),

    # Auth

    path('myaccount/', myaccount, name='myaccount'),
    path('signup/', signup, name='signup'),
    path('login/', views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', logout, name='logout'),

    # API
    path('api/initiate_payment/', initiate_payment, name='initiate_payment'),
    path('api/verify_payment/<str:ref>/', verify_payment, name='verify_payment'),
    path('api/can_use/', api_can_use, name='api_can_use'),
    path('api/create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/add_subscriber/', api_add_subscriber, name='api_add_subscriber'),
    
  

    #Store
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('store/category/<slug:slug>/', category_detail, name='category_detail'),

    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
