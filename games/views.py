from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Game
from .serializers import GameSerializer

@api_view(['POST','GET'])
def store_game_data(request):
    # Store game data sent from the React frontend
    serializer = GameSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_game_data(request, user_id):
    # Retrieve all games played by a user
    games = Game.objects.filter(user__id=user_id)
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)