from django.urls import path
from .views import home,signup_view, login_view, UserList, UserDetail

urlpatterns = [
     path('', home, name='home'), 
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
