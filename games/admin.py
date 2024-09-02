# game/admin.py

from django.contrib import admin
from .models import Item, Category, GameSession

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(GameSession)
