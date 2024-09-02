from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from sweatapi.models import WorkoutType, User, Workout, Type
from django.utils import timezone
from datetime import timedelta

class TypeTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.type_instance = Type.objects.create(type_name='Cardio')
        cls.user = User.objects.create(username='testuser', email='testuser@example.com', uid='testuid')
        cls.workout = Workout.objects.create(
            user=cls.user,
            date=timezone.now().date(),
            duration=timedelta(minutes=30),
            intensity=5
        )
        cls.workout_type = WorkoutType.objects.create(
            workout=cls.workout,
            type=cls.type_instance
        )

    def test_create_workout_type(self):
        url = reverse('type-list')  # Ensure this URL is correct for creating WorkoutType
        new_workout_type = {
            "workout": self.workout.id,
            "type": self.type_instance.id  # Ensure this is correct
        }
        response = self.client.post(url, new_workout_type, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["workout"], new_workout_type["workout"])
        self.assertEqual(data["type"], new_workout_type["type"])




    def test_update_workout_type(self):
        url = reverse('type-detail', kwargs={'pk': self.workout_type.id})
        # Create a new Type instance for update
        new_type_instance = Type.objects.create(type_name='Cardio')
        updated_workout_type = {
            "type": new_type_instance.id  # Use the ID for ForeignKey
        }
        response = self.client.put(url, updated_workout_type, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        # Ensure the correct field is checked
        self.assertEqual(data["type_name"], new_type_instance.id)

        db_workout_type = WorkoutType.objects.get(pk=self.workout_type.id)
        # Since 'type' is a ForeignKey, access it as a related instance
        self.assertEqual(db_workout_type.type.id, new_type_instance.id)



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
        self.assertTrue("type_name" in single_workout_type)

    def test_workout_type_details(self):
        url = reverse('type-detail', kwargs={'pk': self.workout_type.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["id"], self.workout_type.id)
        self.assertEqual(data["type_name"], self.workout_type.type.type_name)
