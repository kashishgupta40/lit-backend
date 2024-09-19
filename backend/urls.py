from django.urls import path
from .views import home,SignupView, LoginView, UserList, UserDetail
from backend import views

urlpatterns = [
     path('', home, name='home'), 
    path('login/', LoginView.as_view(), name='signup'),
    path('signup/', SignupView.as_view(), name='login'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]