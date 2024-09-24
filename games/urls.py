from django.urls import path
from .views import compare_items,leaderboard
from games import views


urlpatterns = [
    path('compare-items/', views.compare_items, name='compare_items'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('game/save-item/', views.save_item, name='save_item'),
    path('game/view-saved-items/', views.view_saved_items, name='view_saved_items'),
    path('friend-list/<str:username>/', views.get_friend_list, name='get_friend_list'),
    path('send-request/<str:receiver_username>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<str:sender_username>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline-request/<str:sender_username>/', views.decline_friend_request, name='decline_friend_request'),
]   