from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sweatapi.models import Workout, WorkoutType, Reflection

class WorkoutViewSet(ViewSet):
    def create(self, request):
        """Handle POST requests to create a new Workout"""
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Workout"""
        try:
            workout = Workout.objects.get(pk=pk)
            serializer = WorkoutSerializer(workout)
            return Response(serializer.data)
        except Workout.DoesNotExist:
            return Response({'message': 'Workout not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all Workouts"""
        workouts = self.get_queryset()
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests to update a Workout"""
        try:
            workout = Workout.objects.get(pk=pk)
        except Workout.DoesNotExist:
            return Response({'message': 'Workout not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the serializer with incoming data
        serializer = WorkoutSerializer(workout, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a Workout"""
        try:
            workout = Workout.objects.get(pk=pk)
            workout.delete()
            return Response({'message': 'Workout deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Workout.DoesNotExist:
            return Response({'message': 'Workout not found'}, status=status.HTTP_404_NOT_FOUND)
          
    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        if user_id:
            return Workout.objects.filter(user_id=user_id)
        return Workout.objects.all()
      

class WorkoutTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutType
        fields = ['id', 'workout', 'type','type_id']
        depth = 2

class ReflectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reflection
        fields = ['id', 'workout', 'mood', 'notes', 'created_on']

class WorkoutSerializer(serializers.ModelSerializer):
    workout_type = serializers.PrimaryKeyRelatedField(queryset=WorkoutType.objects.all())
    reflections = ReflectionSerializer(source='reflection_set', many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'user', 'date', 'duration', 'intensity', 'workout_type', 'reflections']

    
