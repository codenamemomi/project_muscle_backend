from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from user.models import CustomUser 


class Exercise(models.Model):
    MUSCLE_GROUPS = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('legs', 'Legs'),
        ('arms', 'Arms'),
        ('shoulders', 'Shoulders'),
        ('core', 'Core'),
        ('full_body', 'Full Body'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
        ('other', 'Other'),
    ]

    EQUIPMENT_CHOICES = [
        ('bodyweight', 'Bodyweight'),
        ('dumbbell', 'Dumbbell'),
        ('barbell', 'Barbell'),
        ('machine', 'Machine'),
        ('kettlebell', 'Kettlebell'),
        ('resistance_band', 'Resistance Band'),
        ('medicine_ball', 'Medicine Ball'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUPS, default='other')
    equipment = models.CharField(max_length=20, choices=EQUIPMENT_CHOICES, default='other')
    difficulty = models.CharField(
        max_length=12, 
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], 
        default='beginner'
    )

    def __str__(self):
        return f"{self.name} ({self.get_muscle_group_display()})"


class Workout(models.Model):
    WORKOUT_NAMES = [
        ('full_body', 'Full Body Workout'),
        ('upper_body', 'Upper Body Strength'),
        ('lower_body', 'Lower Body Strength'),
        ('push_day', 'Push Day'),
        ('pull_day', 'Pull Day'),
        ('cardio_blast', 'Cardio Blast'),
        ('yoga_session', 'Yoga Session'),
        ('custom', 'Custom'),
    ]

    WORKOUT_TYPES = [
        ('strength', 'Strength Training'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
        ('hiit', 'HIIT'),
        ('powerlifting', 'Powerlifting'),
        ('olympic_lifting', 'Olympic Lifting'),
        ('calisthenics', 'Calisthenics'),
        ('crossfit', 'CrossFit'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=WORKOUT_NAMES, default='custom')  
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES, default='other')
    exercises = models.ManyToManyField(Exercise, related_name="workouts")
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_name_display()} - {self.get_workout_type_display()} ({self.user.full_name})"


User = get_user_model()


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    @property
    def duration(self):
        """Calculates duration in minutes when end_time is set."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() // 60
        return None  # Workout is still ongoing

    def stop_workout(self):
        """Stops the workout and sets end_time."""
        self.end_time = now()
        self.save()

    def __str__(self):
        status = "Ongoing" if not self.end_time else f"{self.duration} min"
        return f"{self.user.full_name} - {self.workout.get_workout_type_display()} ({status})"


class WorkoutExerciseLog(models.Model):
    workout_log = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=3)
    repetitions = models.IntegerField(default=10)
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight used in kg"
    )

    def __str__(self):
        return f"{self.exercise.name} - {self.sets} sets x {self.repetitions} reps"
