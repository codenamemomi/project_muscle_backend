# Generated by Django 5.1.7 on 2025-03-30 20:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('muscle_group', models.CharField(choices=[('chest', 'Chest'), ('back', 'Back'), ('legs', 'Legs'), ('arms', 'Arms'), ('shoulders', 'Shoulders'), ('core', 'Core'), ('full_body', 'Full Body'), ('cardio', 'Cardio'), ('flexibility', 'Flexibility'), ('other', 'Other')], default='other', max_length=20)),
                ('equipment', models.CharField(choices=[('bodyweight', 'Bodyweight'), ('dumbbell', 'Dumbbell'), ('barbell', 'Barbell'), ('machine', 'Machine'), ('kettlebell', 'Kettlebell'), ('resistance_band', 'Resistance Band'), ('medicine_ball', 'Medicine Ball'), ('other', 'Other')], default='other', max_length=20)),
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('full_body', 'Full Body Workout'), ('upper_body', 'Upper Body Strength'), ('lower_body', 'Lower Body Strength'), ('push_day', 'Push Day'), ('pull_day', 'Pull Day'), ('cardio_blast', 'Cardio Blast'), ('yoga_session', 'Yoga Session'), ('custom', 'Custom')], default='custom', max_length=50)),
                ('workout_type', models.CharField(choices=[('strength', 'Strength Training'), ('cardio', 'Cardio'), ('flexibility', 'Flexibility'), ('hiit', 'HIIT'), ('powerlifting', 'Powerlifting'), ('olympic_lifting', 'Olympic Lifting'), ('calisthenics', 'Calisthenics'), ('crossfit', 'CrossFit'), ('other', 'Other')], default='other', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('exercises', models.ManyToManyField(related_name='workouts', to='workout.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.workout')),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutExerciseLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sets', models.IntegerField(default=3)),
                ('repetitions', models.IntegerField(default=10)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, help_text='Weight used in kg', max_digits=5, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.exercise')),
                ('workout_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.workoutlog')),
            ],
        ),
    ]
