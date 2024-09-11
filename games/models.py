from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gamedomain = models.CharField(max_length=100)
    correct_one_picked = models.JSONField()  # Store correct picks as a list
    wrong_one_picked = models.JSONField()    # Store wrong picks as a list
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.email} - {self.gamedomain}"