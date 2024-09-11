from django.urls import path
from .views import store_game_data, get_game_data
from games import views



urlpatterns = [
    path('store-game/', views.store_game_data, name='store_game'),
    path('get-games/<int:user_id>/', views.get_game_data, name='get_games'),
]   