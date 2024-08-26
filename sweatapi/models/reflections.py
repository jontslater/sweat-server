from django.db import models
from .workout import Workout

class Reflection(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    mood = models.IntegerField()
    notes = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Reflection for Workout {self.workout.id}'
