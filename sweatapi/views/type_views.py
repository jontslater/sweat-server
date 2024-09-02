from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sweatapi.models import Type, WorkoutType

class TypeViewSet(ViewSet):
    def create(self, request):
        """Handle POST requests to create a new Type"""
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Type"""
        try:
            type_instance = Type.objects.get(pk=pk)
            serializer = TypeSerializer(type_instance)
            return Response(serializer.data)
        except Type.DoesNotExist:
            return Response({'message': 'Type not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all Types"""
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests to update a Type"""
        try:
            type_instance = Type.objects.get(pk=pk)
            serializer = TypeSerializer(type_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Type.DoesNotExist:
            return Response({'message': 'Type not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a Type"""
        try:
            type_instance = Type.objects.get(pk=pk)
            type_instance.delete()
            return Response({'message': 'Type deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Type.DoesNotExist:
            return Response({'message': 'Type not found'}, status=status.HTTP_404_NOT_FOUND)

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'type_name']
class WorkoutTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutType
        fields = ['id', 'workout', 'type','type_id']
