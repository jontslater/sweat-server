from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from sweatapi.models.profile import Profile
from sweatapi.models.user import User

class ProfileViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='testuser@example.com', uid='testuid')
        self.profile = Profile.objects.create(
            user=self.user,
            age=30,
            gender='Male',
            weight=70,
            height=180,
            goal='Fitness'
        )

    def test_create_profile(self):
        url = reverse('profile-list')
        new_profile = {
            "user": self.user.id,
            "age": 25,
            "gender": "Female",
            "weight": 60,
            "height": 170,
            "goal": "Wellness"
        }
        response = self.client.post(url, new_profile, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["age"], new_profile["age"])
        self.assertEqual(data["gender"], new_profile["gender"])
        self.assertEqual(data["weight"], new_profile["weight"])
        self.assertEqual(data["height"], new_profile["height"])
        self.assertEqual(data["goal"], new_profile["goal"])

    def test_update_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        updated_profile = {
            "age": 35,
            "goal": "Strength Training"
        }
        response = self.client.put(url, updated_profile, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["age"], updated_profile["age"])
        self.assertEqual(data["goal"], updated_profile["goal"])

        # Refresh the profile from the database to ensure changes are saved
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.age, updated_profile["age"])
        self.assertEqual(self.profile.goal, updated_profile["goal"])

    def test_delete_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(id=self.profile.id).exists())

    def test_list_profiles(self):
        url = reverse('profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)
        single_profile = data[0]
        self.assertTrue("id" in single_profile)
        self.assertTrue("user" in single_profile)
        self.assertTrue("age" in single_profile)
        self.assertTrue("gender" in single_profile)
        self.assertTrue("weight" in single_profile)
        self.assertTrue("height" in single_profile)
        self.assertTrue("goal" in single_profile)
