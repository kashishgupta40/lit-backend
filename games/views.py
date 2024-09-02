# from django.shortcuts import render

# from rest_framework import viewsets
# from .models import User, Product, GameSession
# from .serializers import UserSerializer, ProductSerializer, GameSessionSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class GameSessionViewSet(viewsets.ModelViewSet):
#     queryset = GameSession.objects.all()
#     serializer_class = GameSessionSerializer

# def index(request):
#     return render(request, 'games/index.html')

# def test_game(request):
#     result = None
#     if request.method == 'POST':
#         user_name = request.POST.get('user')
#         product1_name = request.POST.get('product1')
#         product2_name = request.POST.get('product2')

#         user = User.objects.get(username=user_name)
#         product1 = Product.objects.get(name=product1_name)
#         product2 = Product.objects.get(name=product2_name)

#         session = GameSession.objects.create(user=user, product1=product1, product2=product2)
#         session.correct_answer = product1.price > product2.price
#         session.save()

#         result = session.correct_answer

#     return render(request, 'games/test_game.html', {'result': result})

from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Item, GameSession, Category
from .serializers import ItemSerializer, GameSessionSerializer

import random

class GameStartView(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        category=get_object_or_404(Category,id=kwargs['category_id'])
        items=list(Item.objects.filter(category=category))
        if len(items)<2:
            return Response({"error":"Not enough items in this category"},status=400)
        
        item1,item2=random.sample(items,2)
        return Response({
            'item1':ItemSerializer(item1).data,
            'item2':ItemSerializer(item2).data,
        })
        
class SubmitChoiceView(generics.CreateAPIView):
    serializer_class=GameSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        item1=get_object_or_404(Item,id=request.data['item1'])
        item2=get_object_or_404(Item,id=request.data['item2'])
        chosen_item=get_object_or_404(Item,id=request.data['chosen_item'])
        correct=chosen_item==max(item1,item2,key=lambda item:item.price)
        
        gmae_session=GameSession.objects.create(
            user=request.user,
            item1=item1,
            item2=item2,
            chosen_item=chosen_item,
            correct=correct
        )
        return({
            "correct":correct,
            'correct_item':ItemSerializer(max(item1,item2,key=lambda item:item.price)).data,
        })