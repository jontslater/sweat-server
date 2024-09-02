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
            user=cls.user,
            date=timezone.now().date(),
            duration=timedelta(minutes=30),
            intensity=5
        )
        cls.workout_type = WorkoutType.objects.create(
            workout=cls.workout,
            type_id=cls.type_instance,  # Assign the Type instance
            type=cls.type_instance.type_name  # Store type_name directly
        )
        cls.reflection = Reflection.objects.create(
            workout=cls.workout,
            mood=4,
            notes='Great workout!',
            created_on=timezone.now()
        )

    def test_workout_type_creation(self):
        url = reverse('type-list')
        new_workout_type = {
            "workout": self.workout.id,
            "type_id": self.type_instance.id,
            "type": "Strength Training"
        }
        response = self.client.post(url, new_workout_type, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["type"], new_workout_type["type"])


        
    def test_delete_workout_type(self):
        url = reverse('type-detail', kwargs={'pk': self.workout_type.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkoutType.objects.filter(id=self.workout_type.id).exists())
        
    def test_list_workout_types(self):
        url = reverse('type-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)
        single_workout_type = data[0]
        self.assertTrue("id" in single_workout_type)
        self.assertTrue("type" in single_workout_type)

    def test_workout_type_details(self):
        url = reverse('type-detail', kwargs={'pk': self.workout_type.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["id"], self.workout_type.id)
