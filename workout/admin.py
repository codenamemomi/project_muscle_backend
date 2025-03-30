from django.contrib import admin
from .models import Workout, WorkoutLog, WorkoutExerciseLog


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "workout_type", "date")
    search_fields = ("name", "workout_type")
    list_filter = ("workout_type", "date")

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "workout", "start_time", "end_time", "duration")
    list_filter = ("start_time", "end_time")
    search_fields = ("user__username", "workout__name")

@admin.register(WorkoutExerciseLog)
class WorkoutExerciseLogAdmin(admin.ModelAdmin):
    list_display = ("id", "workout_log", "exercise", "sets", "repetitions", "weight")
    search_fields = ("exercise__name", "workout_log__workout__name")
    list_filter = ("exercise",)

