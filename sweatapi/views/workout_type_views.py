from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sweatapi.models import WorkoutType, Type,Workout

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'type_name'] 
        depth = 2          
class WorkoutTypeSerializer(serializers.ModelSerializer):
    workout = serializers.PrimaryKeyRelatedField(queryset=Workout.objects.all())
    type_id = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all())
    type = serializers.StringRelatedField()  # Adjust this if needed

    class Meta:
        model = WorkoutType
        fields = ['id', 'workout', 'type_id', 'type']
        depth = 2

class WorkoutTypeViewSet(ViewSet):
    queryset = WorkoutType.objects.all()
    serializer_class = WorkoutTypeSerializer
    
    def create(self, request):
        """Handle POST requests to create a new WorkoutType"""
        serializer = WorkoutTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single WorkoutType"""
        try:
            workout_type = WorkoutType.objects.get(pk=pk)
            serializer = WorkoutTypeSerializer(workout_type)
            return Response(serializer.data)
        except WorkoutType.DoesNotExist:
            return Response({'message': 'WorkoutType not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all WorkoutTypes"""
        workout_types = WorkoutType.objects.all()
        serializer = WorkoutTypeSerializer(workout_types, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a WorkoutType"""
        try:
            workout_type = WorkoutType.objects.get(pk=pk)
            workout_type.delete()
            return Response({'message': 'WorkoutType deleted'}, status=status.HTTP_204_NO_CONTENT)
        except WorkoutType.DoesNotExist:
            return Response({'message': 'WorkoutType not found'}, status=status.HTTP_404_NOT_FOUND)
