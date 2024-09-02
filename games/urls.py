from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import GameStartView, SubmitChoiceView

# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'products', ProductViewSet)
# router.register(r'gamesessions', GameSessionViewSet)

urlpatterns = [
    # path('', index, name='index'),
    # path('', include(router.urls)),
    # path('test_game/', views.test_game, name='test_game'),
    # path('api/', include(router.urls)),
    path('start/<int:category_id>/', GameStartView.as_view(), name='game-start'),
    path('submit/', SubmitChoiceView.as_view(), name='game-submit'),
]
