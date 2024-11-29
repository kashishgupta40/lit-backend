
from django.urls import path
from . import views

urlpatterns = [
    # Django REST API views
    path('api/cart/add/<int:product_id>/', views.api_add_to_cart, name='api_add_to_cart'),
    path('api/cart/remove/<int:product_id>/', views.api_remove_from_cart, name='api_remove_from_cart'),
    path('api/cart/', views.api_view_cart, name='api_view_cart'),
    path('api/order/place/', views.api_place_order, name='api_place_order'),
]


