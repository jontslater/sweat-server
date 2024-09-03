from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from sweatapi.models import WorkoutType, User, Workout, Type, Reflection
from django.utils import timezone
from datetime import timedelta

class WorkoutTypeTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.type_instance = Type.objects.create(type_name='Cardio')
        cls.user = User.objects.create(username='testuser')
       
        cls.workout = Workout.objects.create(
            id=1,
            user=cls.user,
            date=timezone.now().date(),
            duration=timedelta(minutes=30),
            intensity=5
        )
        
        cls.workout_type = WorkoutType.objects.create(
            workout=cls.workout,
            type=cls.type_instance
        )
        
        cls.reflection = Reflection.objects.create(
            workout=cls.workout,
            mood=4,
            notes='Great workout!',
            created_on=timezone.now()
        )

    def test_delete_workout_type(self):
        url = reverse('workouttype-detail', kwargs={'pk': self.workout_type.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkoutType.objects.filter(id=self.workout_type.id).exists())
    
