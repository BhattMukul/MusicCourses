from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:course_id>', views.add_cart, name='cart_add'),
    path('', views.CartDetail, name='cart_detail'),
    path('delete/', views.cart_empty, name='cart_delete'),
]
