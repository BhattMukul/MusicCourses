from django.urls import path
from .views import add_wish, remove_wish, wishlistview


app_name = 'wishlist'

urlpatterns = [
    path('', wishlistview, name='main_wishlist'),
    path('add/<int:id>/<slug:slug>/', add_wish, name='add_wish'),
    path('remove/<int:id>/<slug:slug>/', remove_wish, name='remove_wish'),
]
