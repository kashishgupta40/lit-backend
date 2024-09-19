from rest_framework import serializers
from .models import UserGameData

class UserGameDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGameData
        fields = ['lives', 'streak', 'last_played', 'score', 'levels_completed', 'lives_reset_time',
                  'footwear_levels', 'clothing_levels', 'bags_level', 'accessories_levels', 'total_games_played', 'total_games_won', 'rank']
