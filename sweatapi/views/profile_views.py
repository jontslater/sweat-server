from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from sweatapi.models import User
from rest_framework import serializers, status
from sweatapi.models import Profile

class ProfileViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests to retrieve a profile"""
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    def list(self, request):
        """Handle GET requests for all profiles"""
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST requests to create a new profile"""
        try:
            profile = Profile.objects.create(
                user_id=request.data["user"],
                age=request.data["age"],
                gender=request.data["gender"],
                weight=request.data["weight"],
                height=request.data["height"],
                goal=request.data["goal"]
            )
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests to update a profile"""
        try:
            profile = Profile.objects.get(pk=pk)
            profile.age = request.data.get('age', profile.age)
            profile.gender = request.data.get('gender', profile.gender)
            profile.weight = request.data.get('weight', profile.weight)
            profile.height = request.data.get('height', profile.height)
            profile.goal = request.data.get('goal', profile.goal)
            profile.save()
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

          
    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a profile"""
        try:
            profile = Profile.objects.get(pk=pk)
            profile.delete()
            return Response({'message': 'Profile deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
      
          
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'age', 'gender', 'weight', 'height', 'goal']
        depth = 2
         
