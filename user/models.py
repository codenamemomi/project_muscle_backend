from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    GOAL_CHOICES = (
        ('weight loss', 'Weight Loss'),
        ('muscle gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('general fitness', 'General Fitness'),
    )

    EXPERIENCE_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    WORKOUT_CHOICES = (
        ('Strength Training', 'Strength Training'),
        ('Cardio', 'Cardio'),
        ('Yoga', 'Yoga'),
        ('Muscle Building', 'Muscle Building'),
        ('Flexibility', 'Flexibility'),
    )

    FREQUENCY_CHOICES = (
        ('Daily', 'Daily'),
        ('6 times a week', '6 times a week'),
        ('5 times a week', '5 times a week'),
        ('4 times a week', '4 times a week'),
        ('3 times a week', '3 times a week'),
        ('2 times a week', '2 times a week'),
        ('Occasionally', 'Occasionally'),
    )
    username = None
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(blank=True, max_length=225)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Fitness & Health Data
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    goal = models.CharField(max_length=50, choices=GOAL_CHOICES, blank=True, null=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True, null=True)
    preferred_workout_type = models.CharField(max_length=50, choices=WORKOUT_CHOICES, blank=True, null=True)
    workout_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
