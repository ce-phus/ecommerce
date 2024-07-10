from django.urls import path

from . import views
from apps.payment.views import verify_payment, initiate_payment

urlpatterns = [
    path('order', initiate_payment, name='start_order'),
    path('verify_payment<str:ref>/', verify_payment, name='verify_payment')
]