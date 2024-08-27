from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sweatapi.models import Reflection

class ReflectionViewSet(ViewSet):
    def create(self, request):
        """Handle POST requests to create a new reflection"""
        serializer = ReflectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single reflection"""
        try:
            reflection = Reflection.objects.get(pk=pk)
            serializer = ReflectionSerializer(reflection)
            return Response(serializer.data)
        except Reflection.DoesNotExist:
            return Response({'message': 'Reflection not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all reflections"""
        reflections = Reflection.objects.all()
        serializer = ReflectionSerializer(reflections, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests to update a reflection"""
        try:
            reflection = Reflection.objects.get(pk=pk)
            serializer = ReflectionSerializer(reflection, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Reflection.DoesNotExist:
            return Response({'message': 'Reflection not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a reflection"""
        try:
            reflection = Reflection.objects.get(pk=pk)
            reflection.delete()
            return Response({'message': 'Reflection deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Reflection.DoesNotExist:
            return Response({'message': 'Reflection not found'}, status=status.HTTP_404_NOT_FOUND)

class ReflectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reflection
        fields = ['id', 'workout', 'mood', 'notes', 'created_on']          
