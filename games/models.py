from django.db import models
from backend.models import CustomUser
from django.conf import settings

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



class SavedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='saved_items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_price = models.CharField(max_length=50)
    item_category = models.CharField(max_length=100)
    item_picture = models.URLField()
    item_link = models.URLField(blank=True, null=True)  # Optional: If you want to provide a link to buy the item
    item_brand = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} saved by {self.user.username}"
