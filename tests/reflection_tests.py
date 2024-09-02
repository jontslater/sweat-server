from sweatapi.models import Reflection, Workout, User
from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import timedelta
import datetime
from rest_framework import status


class ReflectionTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testuser', email='testuser@example.com', uid='testuid')

        cls.workout = Workout.objects.create(
            user=cls.user,
            date='2024-08-30',
            duration=timedelta(minutes=30),
            intensity='5',
        )
        cls.reflection = Reflection.objects.create(
            workout=cls.workout,
            mood=4,
            notes='Great workout!',
            created_on='2024-08-30'
        )

    def test_create_reflection(self):
        url = reverse('reflection-list')  # Use reverse to get the URL
        new_reflection = {
            "workout": self.workout.id,
            "mood": 5,
            "notes": "Amazing workout!",
        }
        response = self.client.post(url, new_reflection, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data

        self.assertTrue("id" in data)
        self.assertEqual(data["mood"], new_reflection["mood"])
        self.assertEqual(data["notes"], new_reflection["notes"])
        self.assertEqual(data["created_on"], datetime.date.today().isoformat())

    def test_update_reflection(self):
        url = reverse('reflection-detail', kwargs={'pk': self.reflection.id})  # Use reverse to get the URL
        updated_reflection = {
            "notes": "Updated notes",
            "mood": 3
        }
        response = self.client.put(url, updated_reflection, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["notes"], updated_reflection["notes"])
        self.assertEqual(data["mood"], updated_reflection["mood"])

        db_reflection = Reflection.objects.get(pk=self.reflection.id)
        self.assertEqual(db_reflection.notes, updated_reflection["notes"])
        self.assertEqual(db_reflection.mood, updated_reflection["mood"])

    def test_delete_reflection(self):
        url = reverse('reflection-detail', kwargs={'pk': self.reflection.id})  # Use reverse to get the URL
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reflection.objects.filter(id=self.reflection.id).exists())
        
    def test_list_reflections(self):
        url = reverse('reflection-list')  # Use reverse to get the URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)
        single_reflection = data[0]
        self.assertTrue("id" in single_reflection)
        self.assertTrue("workout" in single_reflection)
        self.assertTrue("mood" in single_reflection)
        self.assertTrue("notes" in single_reflection)
        self.assertTrue("created_on" in single_reflection)

    def test_reflection_details(self):
        url = reverse('reflection-detail', kwargs={'pk': self.reflection.id})  # Use reverse to get the URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["id"], self.reflection.id)
        self.assertEqual(data["mood"], self.reflection.mood)
        self.assertEqual(data["notes"], self.reflection.notes)
        self.assertEqual(data["created_on"], str(self.reflection.created_on))
