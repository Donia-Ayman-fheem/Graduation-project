from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile, Gender, FitnessGoal
from diet_plans.serializers import DietPlanListSerializer
from workouts.serializers import WorkoutPlanListSerializer

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    fitness_goal_display = serializers.CharField(source='get_fitness_goal_display', read_only=True)
    diet_plan_details = DietPlanListSerializer(source='diet_plan', read_only=True)
    workout_plan_details = WorkoutPlanListSerializer(source='workout_plan', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'image', 'age', 'gender', 'gender_display', 'fitness_goal',
            'fitness_goal_display', 'diet_plan', 'diet_plan_details',
            'workout_plan', 'workout_plan_details', 'height', 'weight',
            'waist_circumference', 'hip_circumference', 'chest_circumference',
            'arm_circumference', 'thigh_circumference', 'neck_circumference',
            'body_photo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'profile', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_active', 'date_joined']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        # Create an empty profile for the user
        Profile.objects.create(user=user)

        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'age', 'gender', 'fitness_goal', 'diet_plan', 'workout_plan']


class BodyMeasurementsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'height', 'weight', 'waist_circumference', 'hip_circumference',
            'chest_circumference', 'arm_circumference', 'thigh_circumference',
            'neck_circumference', 'body_photo'
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = ['name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update user fields
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Update profile fields
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
