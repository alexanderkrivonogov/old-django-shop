from django.urls import path

from cart import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<comics_id>/', views.cart_add, name='cart_add'),
    path('remove/<comics_id>/', views.cart_remove, name='cart_remove'),
]