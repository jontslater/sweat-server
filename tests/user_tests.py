from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from sweatapi.models import User

class UserTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            uid='testuid'
        )

    def test_create_user(self):
        url = reverse('user-list')  # Use reverse to get the URL for listing users
        new_user = {
            "username": "newuser",
            "email": "newuser@example.com",
            "uid": "newuid"
        }
        response = self.client.post(url, new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertTrue("id" in data)
        self.assertEqual(data["username"], new_user["username"])
        self.assertEqual(data["email"], new_user["email"])
        self.assertEqual(data["uid"], new_user["uid"])

    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})  # Use reverse to get the URL for a specific user
        updated_user = {
            "username": "updateduser",
            "email": "updateduser@example.com",
        }
        response = self.client.put(url, updated_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["username"], updated_user["username"])
        self.assertEqual(data["email"], updated_user["email"])

        db_user = User.objects.get(pk=self.user.id)
        self.assertEqual(db_user.username, updated_user["username"])
        self.assertEqual(db_user.email, updated_user["email"])
        
    def test_list_users(self):
        url = reverse('user-list')  # Use reverse to get the URL for listing users
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)
        single_user = data[0]
        self.assertTrue("id" in single_user)
        self.assertTrue("username" in single_user)
        self.assertTrue("email" in single_user)
