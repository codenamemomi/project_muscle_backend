from rest_framework import serializers
from .models import Exercise, Workout, WorkoutLog, WorkoutExerciseLog

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description']  

class WorkoutSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    exercises = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(), many=True, required=True
    )
    class Meta:
        model = Workout
        fields = '__all__'

class WorkoutLogSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer(read_only=True)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutLog
        fields = '__all__'

    def get_duration(self, obj):
        if obj.start_time and obj.end_time:
            return (obj.end_time - obj.start_time).total_seconds() // 60  # Convert to minutes
        return None

class WorkoutExerciseLogSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExerciseLog
        fields = '__all__'
