# game/admin.py

from django.contrib import admin
from .models import CustomUser
from .models import UserGameData ,FriendList, FriendRequest,SavedItem

admin.site.register(CustomUser)
admin.site.register(UserGameData)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(SavedItem)
