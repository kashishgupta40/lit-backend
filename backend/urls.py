from django.urls import path
from .views import home,signup, login, UserList, UserDetail
from backend import views

urlpatterns = [
     path('', home, name='home'), 
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]