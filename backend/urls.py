from django.urls import path
from .views import home,signup, login, UserList, UserDetail

urlpatterns = [
     path('', home, name='home'), 
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]