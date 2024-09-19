from django.db import models
# from django.contrib.auth.models import User
from backend.models import CustomUser

class UserGameData(models.Model):
    CustomUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    lives = models.IntegerField(default=5)
    streak = models.IntegerField(default=0)
    last_played = models.DateField(null=True, blank=True)
    score = models.IntegerField(default=0)
    levels_completed = models.IntegerField(default=0)
    lives_reset_time = models.DateTimeField(null=True, blank=True)  
    footwear_levels = models.IntegerField(default=0)
    clothing_levels = models.IntegerField(default=0)
    bags_levels = models.IntegerField(default=0)
    accessories_levels = models.IntegerField(default=0)
    total_games_played = models.IntegerField(default=0)
    total_games_won = models.IntegerField(default=0)
    rank = models.CharField(max_length=20, default='Beginner')
    
    def __str__(self):
        return f"{self.user.username}'s Game Data"
