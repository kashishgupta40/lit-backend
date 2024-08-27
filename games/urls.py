from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProductViewSet, GameSessionViewSet, index

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'gamesessions', GameSessionViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
]
