from django.db import models
from .workout import Workout
from .type import Type

class WorkoutType(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('workout', 'type')

    def __str__(self):
        return f'{self.workout} - {self.type}'
