from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta
from django.urls import reverse
import datetime
from django.utils import timezone
from sweatapi.models import Workout, WorkoutType, Reflection, Type, User

class WorkoutTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a Type instance
        cls.workout_type_instance = Type.objects.create(type_name='Cardio')

        # Create a User instance
        cls.user = User.objects.create(username='testuser')

        # Create a Workout instance
        cls.workout = Workout.objects.create(
            user=cls.user,
            date=timezone.now().date(),
            duration=timedelta(minutes=30),
            intensity=5
        )

        # Create a WorkoutType instance
        cls.workout_type = WorkoutType.objects.create(
            workout=cls.workout,
            type=cls.workout_type_instance
        )
        
        # Create a Reflection instance
        cls.reflection = Reflection.objects.create(
            workout=cls.workout,
            mood=4,
            notes='Great workout!',
            created_on=timezone.now()
        )


    def test_create_workout(self):
        current_date = datetime.date.today().isoformat()
        
        new_workout = {
            "user": self.user.id,
            # Remove 'date' from the payload
            "duration": "01:30:00",
            "intensity": 6,
            "type": 1,
            'workout_type': self.workout_type.id
        }
        
        response = self.client.post(reverse('workout-list'), new_workout, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data

        self.assertTrue("id" in data)
        self.assertEqual(data["user"], new_workout["user"])
        self.assertEqual(data["duration"], new_workout["duration"])
        self.assertEqual(data["intensity"], new_workout["intensity"])
        self.assertEqual(data["date"], current_date)
        self.assertEqual(data["workout_type"], new_workout["workout_type"])

    def test_update_workout(self):
        workout_id = self.workout.id
        updated_duration = datetime.timedelta(hours=2)
        updated_workout = {
            "duration": "02:00:00",
            "intensity": 7,
            "workout_type": 1,
            "reflection": 1
        }
        
        response = self.client.put(reverse('workout-detail', args=[workout_id]), updated_workout, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        response_duration = datetime.timedelta(
            hours=int(data["duration"].split(":")[0]),
            minutes=int(data["duration"].split(":")[1]),
            seconds=int(data["duration"].split(":")[2])
        )
        
        self.assertEqual(response_duration, updated_duration)
        self.assertEqual(data["intensity"], updated_workout["intensity"])

        db_workout = Workout.objects.get(pk=workout_id)
        self.assertEqual(db_workout.duration, updated_duration)
        self.assertEqual(db_workout.intensity, updated_workout["intensity"])

    def test_delete_workout(self):
        workout_id = self.workout.id
        response = self.client.delete(f"/workouts/{workout_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Workout.objects.filter(id=workout_id).exists())
        
    def test_list_workouts(self):
        response = self.client.get("/workouts")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)
        single_workout = data[0]
        self.assertTrue("id" in single_workout)
        self.assertTrue("user" in single_workout)
        self.assertTrue("date" in single_workout)
        self.assertTrue("duration" in single_workout)
        self.assertTrue("intensity" in single_workout)
        self.assertTrue("reflections" in single_workout)

    def test_workout_details(self):
        workout = self.workout
        response = self.client.get(f"/workouts/{workout.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["id"], workout.id)
        self.assertEqual(data["date"], str(workout.date))
        expected_duration = str(workout.duration)
        response_duration = data["duration"]
        normalized_expected_duration = expected_duration.zfill(8)
        normalized_response_duration = response_duration.zfill(8)
        
        self.assertEqual(normalized_response_duration, normalized_expected_duration)
        
        self.assertEqual(data["intensity"], workout.intensity)
        self.assertEqual(data["reflections"][0]["id"], self.reflection.id)
