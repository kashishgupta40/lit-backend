from django.db import models
from backend.models import CustomUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone




class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    dob = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change this to something unique
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change this to something unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )



class UserGameData(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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

    class Meta:
        db_table = 'games_UserGameData'
    
    def __str__(self):
        
        return f"{self.custom_user.username}'s Game Data"
            



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
    

class FriendList(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='friend_list')
    friends = models.ManyToManyField(CustomUser, related_name='friends', blank=True)

    def __str__(self):
        return f"{self.user.username}'s friends"
    
    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def is_friend(self, account):
        return account in self.friends.all()


class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_requests')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
            self.is_active = False
            self.save()

    def decline(self):
        self.is_active = False
        self.save()        




class Leaderboard(models.Model):
   
    score = models.IntegerField()
    player_name = models.CharField(max_length=255)
    rank = models.IntegerField()
    total_games_played = models.IntegerField()
    total_games_won = models.IntegerField()
    last_played = models.DateTimeField(null=True, blank=True)
    levels_completed = models.IntegerField()
    lives = models.IntegerField()
    streak = models.IntegerField()
    footwear_levels = models.IntegerField()
    clothing_levels = models.IntegerField()
    bags_levels = models.IntegerField()
    accessories_levels = models.IntegerField()
    