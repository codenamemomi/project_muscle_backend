from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'bio', 'profile_picture', 'phone_number', 
                  'date_of_birth', 'height', 'weight', 'goal', 'experience_level', 
                  'preferred_workout_type', 'workout_frequency', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password as it's not needed in the model
        
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data.get('full_name', ''),
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None),
            phone_number=validated_data.get('phone_number', ''),
            date_of_birth=validated_data.get('date_of_birth', None),
            height=validated_data.get('height', None),
            weight=validated_data.get('weight', None),
            goal=validated_data.get('goal', ''),
            experience_level=validated_data.get('experience_level', ''),
            preferred_workout_type=validated_data.get('preferred_workout_type', ''),
            workout_frequency=validated_data.get('workout_frequency', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return {
            "refresh": str(refresh),
            "access": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
            },
        }

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "full_name"]
        extra_kwargs = {
            "email": {"required": False},
            "username": {"required": False},
            "full_name": {"required": False},
        }
