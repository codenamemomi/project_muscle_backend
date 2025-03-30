from django.urls import path
from .views import StartWorkoutView, StopWorkoutView, WorkoutLogListView, CreateWorkoutView

urlpatterns = [
    path('workouts/create/', CreateWorkoutView.as_view(), name='create-workout'),
    path('workouts/start/', StartWorkoutView.as_view(), name='start_workout'),
    path('workouts/stop/', StopWorkoutView.as_view(), name='stop_workout'),
    path('workouts/logs/', WorkoutLogListView.as_view(), name='workout_logs'),
]
