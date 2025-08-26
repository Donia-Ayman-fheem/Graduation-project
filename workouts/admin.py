from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise,
    UserWorkout, VideoTutorial, SavedVideo, VideoCategory
)


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1
    fields = ('exercise', 'order', 'sets', 'reps', 'rest_seconds')


class WorkoutDayInline(admin.TabularInline):
    model = WorkoutDay
    extra = 1
    fields = ('day_number', 'name', 'description', 'rest_day')


class VideoTutorialInline(admin.TabularInline):
    model = VideoTutorial
    extra = 1
    fields = ('title', 'video_url', 'duration_minutes', 'duration_seconds', 'order', 'is_featured')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_part', 'difficulty', 'equipment_needed')
    list_filter = ('body_part', 'difficulty', 'equipment_needed')
    search_fields = ('name', 'description', 'instructions')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'body_part', 'difficulty', 'image')
        }),
        (_('Exercise Details'), {
            'fields': ('instructions', 'tips', 'video_url')
        }),
        (_('Equipment'), {
            'fields': ('equipment_needed', 'equipment_description')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty', 'duration_weeks', 'sessions_per_week', 'is_featured', 'is_active')
    list_filter = ('category', 'difficulty', 'is_featured', 'is_active')
    search_fields = ('name', 'description', 'goal')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WorkoutDayInline, VideoTutorialInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'difficulty', 'image')
        }),
        (_('Plan Details'), {
            'fields': ('duration_weeks', 'sessions_per_week', 'minutes_per_session', 'goal')
        }),
        (_('Status'), {
            'fields': ('is_featured', 'is_active')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = ('workout_plan', 'day_number', 'name', 'rest_day')
    list_filter = ('workout_plan', 'rest_day')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WorkoutExerciseInline]

    fieldsets = (
        (None, {
            'fields': ('workout_plan', 'day_number', 'name', 'rest_day')
        }),
        (_('Details'), {
            'fields': ('description',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(VideoTutorial)
class VideoTutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'workout_plan', 'duration_minutes', 'duration_seconds', 'order', 'is_featured', 'is_active')
    list_filter = ('workout_plan', 'is_featured', 'is_active')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'workout_plan', 'video_url', 'thumbnail')
        }),
        (_('Duration'), {
            'fields': ('duration_minutes', 'duration_seconds')
        }),
        (_('Display Options'), {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(SavedVideo)
class SavedVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'source_type', 'is_favorite', 'created_at')
    list_filter = ('category', 'source_type', 'is_favorite')
    search_fields = ('title', 'description', 'user__name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'video_url', 'thumbnail')
        }),
        (_('Classification'), {
            'fields': ('category', 'is_favorite')
        }),
        (_('Duration'), {
            'fields': ('duration_minutes', 'duration_seconds')
        }),
        (_('Source Information'), {
            'fields': ('source_type', 'source_id', 'notes')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(UserWorkout)
class UserWorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_plan', 'start_date', 'is_active', 'completed')
    list_filter = ('is_active', 'completed', 'start_date')
    search_fields = ('user__name', 'user__email', 'workout_plan__name', 'notes')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'workout_plan', 'start_date')
        }),
        (_('Status'), {
            'fields': ('is_active', 'completed', 'notes')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
