# game/admin.py

from django.contrib import admin
from .models import UserGameData

admin.site.register(UserGameData)