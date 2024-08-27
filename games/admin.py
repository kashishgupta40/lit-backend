from django.contrib import admin
from .models import User, Product, GameSession

admin.site.register(User)
admin.site.register(Product)
admin.site.register(GameSession)
