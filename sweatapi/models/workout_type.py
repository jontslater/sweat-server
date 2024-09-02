from django.db import models
from .workout import Workout
from .type import Type

class WorkoutType(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=255)

    class Meta:
        unique_together = ('workout', 'type_id', 'type')

    def __str__(self):
        return f'{self.workout} - {self.type}'
