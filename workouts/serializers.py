from rest_framework import serializers
from .models import (
    Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise,
    UserWorkout, VideoTutorial, SavedVideo, VideoCategory
)


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for exercises
    """
    body_part_display = serializers.CharField(source='get_body_part_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'description', 'body_part', 'body_part_display',
            'difficulty', 'difficulty_display', 'instructions', 'tips',
            'image', 'video_url', 'equipment_needed', 'equipment_description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for workout exercises
    """
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = [
            'id', 'exercise', 'order', 'sets', 'reps',
            'rest_seconds', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutDaySerializer(serializers.ModelSerializer):
    """
    Serializer for workout days
    """
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutDay
        fields = [
            'id', 'day_number', 'name', 'description',
            'rest_day', 'exercises', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutPlanListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing workout plans
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    days_count = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutPlan
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'difficulty', 'difficulty_display', 'duration_weeks',
            'sessions_per_week', 'minutes_per_session', 'image',
            'days_count', 'is_featured', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_days_count(self, obj):
        return obj.days.count()


class VideoTutorialSerializer(serializers.ModelSerializer):
    """
    Serializer for video tutorials
    """
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)

    class Meta:
        model = VideoTutorial
        fields = [
            'id', 'title', 'description', 'video_url', 'duration_minutes',
            'duration_seconds', 'duration_display', 'thumbnail', 'order',
            'is_featured', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutPlanDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed workout plan information
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    days = WorkoutDaySerializer(many=True, read_only=True)
    video_tutorials = VideoTutorialSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'difficulty', 'difficulty_display', 'duration_weeks',
            'sessions_per_week', 'minutes_per_session', 'goal',
            'image', 'days', 'video_tutorials', 'is_featured', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SavedVideoSerializer(serializers.ModelSerializer):
    """
    Serializer for saved videos
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)
    source_type_display = serializers.SerializerMethodField()

    class Meta:
        model = SavedVideo
        fields = [
            'id', 'title', 'description', 'video_url', 'category',
            'category_display', 'duration_minutes', 'duration_seconds',
            'duration_display', 'thumbnail', 'is_favorite', 'notes',
            'source_type', 'source_type_display', 'source_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_source_type_display(self, obj):
        source_types = {
            'tutorial': 'Workout Tutorial',
            'external': 'External Video',
            'custom': 'Custom Upload'
        }
        return source_types.get(obj.source_type, obj.source_type)


class SavedVideoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating saved videos
    """
    class Meta:
        model = SavedVideo
        fields = [
            'title', 'description', 'video_url', 'category',
            'duration_minutes', 'duration_seconds', 'thumbnail',
            'is_favorite', 'notes', 'source_type', 'source_id'
        ]

    def create(self, validated_data):
        # Get the current user from the context
        user = self.context['request'].user
        # Create the saved video with the user
        return SavedVideo.objects.create(user=user, **validated_data)


class UserWorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for user workouts
    """
    workout_plan = WorkoutPlanListSerializer(read_only=True)
    workout_plan_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutPlan.objects.filter(is_active=True),
        write_only=True,
        source='workout_plan'
    )

    class Meta:
        model = UserWorkout
        fields = [
            'id', 'workout_plan', 'workout_plan_id', 'start_date',
            'is_active', 'completed', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'start_date', 'created_at', 'updated_at']
