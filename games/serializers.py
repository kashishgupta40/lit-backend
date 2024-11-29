from rest_framework import serializers
from .models import UserGameData,SavedItem

class UserGameDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGameData
        fields = ['custom_user', 'lives', 'streak', 'last_played', 'score', 'levels_completed', 'lives_reset_time',
                  'footwear_levels', 'clothing_levels', 'bags_levels', 'accessories_levels', 'total_games_played', 'total_games_won', 'rank']
    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Score must be a positive number.")
        return value



class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='custom_user.username')  

    class Meta:
        model = UserGameData
        fields = ['username', 'score', 'total_games_won', 'total_games_played']

class SavedItemSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username') 
    class Meta:
        model=SavedItem
        fields=['id', 'item_name', 'item_price', 'item_category', 'item_picture', 'item_link', 'item_brand', 'created_at']