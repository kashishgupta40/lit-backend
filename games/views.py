from django.shortcuts import render

from rest_framework import viewsets
from .models import User, Product, GameSession
from .serializers import UserSerializer, ProductSerializer, GameSessionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer

def index(request):
    return render(request, 'games/index.html')