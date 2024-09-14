from django.urls import path
from .views import compare_items
from games import views


urlpatterns = [
    path('compare-items/', views.compare_items, name='compare_items'),
]   