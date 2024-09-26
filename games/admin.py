# game/admin.py

from django.contrib import admin
from .models import UserGameData ,FriendList, FriendRequest

admin.site.register(UserGameData)
admin.site.register(FriendList)
admin.site.register(FriendRequest)