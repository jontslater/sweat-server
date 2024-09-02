from django.db import models
from .user import User


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField(auto_now_add=True)
    duration = models.DurationField()
    intensity = models.IntegerField()
    workout_type = models.ForeignKey('WorkoutType', on_delete=models.CASCADE, related_name='workouts', blank=True, null=True)

    def __str__(self):
        return f'Workout {self.id} for {self.user.username}'



    def __str__(self):
        return f'Workout {self.id} for {self.user.username}'
