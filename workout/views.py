from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Workout, WorkoutLog
from .serializers import WorkoutSerializer, WorkoutLogSerializer

class CreateWorkoutView(generics.CreateAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 🏋️‍♂️ Start a workout (Only one active workout at a time)
class StartWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        workout_id = request.data.get('workout_id')

        # Check if the user already has an active workout
        active_workout = WorkoutLog.objects.filter(user=user, end_time__isnull=True).first()
        if active_workout:
            return Response(
                {"error": "You already have an active workout. Stop it before starting a new one."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            workout = Workout.objects.get(id=workout_id, user=user)
        except Workout.DoesNotExist:
            return Response({"error": "Workout not found"}, status=status.HTTP_404_NOT_FOUND)

        workout_log = WorkoutLog.objects.create(
            user=user,
            workout=workout,
            start_time=now()
        )
        return Response({"message": "Workout started", "log_id": workout_log.id}, status=status.HTTP_201_CREATED)


# ⏹️ Stop the currently active workout
class StopWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Find the active workout (where `end_time` is NULL)
        workout_log = WorkoutLog.objects.filter(user=user, end_time__isnull=True).first()

        if not workout_log:
            return Response({"error": "No active workout found to stop."}, status=status.HTTP_400_BAD_REQUEST)

        workout_log.stop_workout()  # Call the method to set `end_time`
        return Response({"message": "Workout stopped", "duration": workout_log.duration}, status=status.HTTP_200_OK)


# 📜 Get all workout logs
class WorkoutLogListView(generics.ListAPIView):
    serializer_class = WorkoutLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutLog.objects.filter(user=self.request.user).order_by('-start_time')
