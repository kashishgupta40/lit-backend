from django.urls import path
from .views import compare_items, leaderboard, add_friend, remove_friend, view_friends, send_friend_request, respond_to_friend_request
from games import views
from .models import Leaderboard
from .views import leaderboard


def leaderboard(request):
    # Logic for handling the request
    leaderboard_data = Leaderboard.objects.all() 
    return render(request,  {'leaderboard_data': leaderboard_data})

leaderboard_response = leaderboard(request)

urlpatterns = [
    path('compare-items/', views.compare_items, name='compare_items'),

    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('game/save-item/', views.save_item, name='save_item'),
    path('game/view-saved-items/', views.view_saved_items, name='view_saved_items'),
    path('add_friend/', add_friend, name='add_friend'),
    path('remove_friend/', remove_friend, name='remove_friend'),
    path('view_friends/<int:user_id>/', view_friends, name='view_friends'),
    path('send_friend_request/', send_friend_request, name='send_friend_request'),
    path('respond_friend_request/', respond_to_friend_request, name='respond_friend_request'),
]   