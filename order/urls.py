from django.urls import path
from .views import order_success, order_unsuccess

app_name = 'order'

urlpatterns = [
    path('success/<int:id>', order_success, name='success'),
    path('unsuccessful/', order_unsuccess, name='order_unsuccess'),
    path('unsuccessful/<str:reason>/', order_unsuccess,
         name='order_unsuccess_with_reason'),
]
