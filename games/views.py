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

def test_game(request):
    result = None
    if request.method == 'POST':
        user_name = request.POST.get('user')
        product1_name = request.POST.get('product1')
        product2_name = request.POST.get('product2')

        user = User.objects.get(username=user_name)
        product1 = Product.objects.get(name=product1_name)
        product2 = Product.objects.get(name=product2_name)

        session = GameSession.objects.create(user=user, product1=product1, product2=product2)
        session.correct_answer = product1.price > product2.price
        session.save()

        result = session.correct_answer

    return render(request, 'games/test_game.html', {'result': result})