from django.db import models
from .user import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')  # ForeignKey to User model
    age = models.IntegerField()
    gender = models.CharField(max_length=55)
    weight = models.IntegerField()
    height = models.IntegerField()
    goal = models.CharField(max_length=255) 

    def __str__(self):
        return f'{self.user.username} - Profile'
