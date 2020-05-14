from django.urls import path
from .views import payment_failure, payment_success, main_payment

app_name = 'payment'

urlpatterns = [
    path('checkout/<int:user_id>/<int:id>/',
         main_payment, name='main_payment'),
    path('Success/', payment_success, name='payment_Success'),
    path('Failure/', payment_failure, name='payment_Failure'),

]
