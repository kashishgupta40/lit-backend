from django.urls import path,include
from .views import home, UserList, UserDetail
from rest_framework.routers import DefaultRouter
from .views import SignupViewSet,LoginViewSet


router = DefaultRouter()
router.register('signup', SignupViewSet, basename='signup')
router.register('login', LoginViewSet, basename='login')



urlpatterns = [
    path('', home, name='home'), 
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('auth/',include(router.urls))
]