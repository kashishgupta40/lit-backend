from django.urls import path
from .views import compare_items,leaderboard
from games import views


urlpatterns = [
    path('compare-items/', views.compare_items, name='compare_items'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]   