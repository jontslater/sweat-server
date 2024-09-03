from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from sweatapi.models import Type

class TypeTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.type_instance = Type.objects.create(type_name='Cardio')

    def test_create_type(self):
        """Test creating a new Type"""
        url = reverse('type-list')  # URL for TypeViewSet's list action
        new_type = {
            "type_name": "Strength"
        }
        response = self.client.post(url, new_type, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['type_name'], new_type['type_name'])

    def test_retrieve_type(self):
        """Test retrieving a single Type"""
        url = reverse('type-detail', kwargs={'pk': self.type_instance.id})  # URL for TypeViewSet's retrieve action
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type_name'], self.type_instance.type_name)

    def test_update_type(self):
        """Test updating an existing Type"""
        url = reverse('type-detail', kwargs={'pk': self.type_instance.id})  # URL for TypeViewSet's update action
        updated_type = {
            "type_name": "Endurance"
        }
        response = self.client.put(url, updated_type, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type_name'], updated_type['type_name'])

    def test_partial_update_type(self):
        url = reverse('type-detail', kwargs={'pk': self.type_instance.id})
        updated_data = {
            "type_name": "Updated Cardio"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["type_name"], updated_data["type_name"])



    def test_delete_type(self):
        """Test deleting a Type"""
        url = reverse('type-detail', kwargs={'pk': self.type_instance.id})  # URL for TypeViewSet's destroy action
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Type.objects.filter(id=self.type_instance.id).exists())

    def test_list_types(self):
        """Test listing all Types"""
        url = reverse('type-list')  # URL for TypeViewSet's list action
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type_name'], self.type_instance.type_name)
