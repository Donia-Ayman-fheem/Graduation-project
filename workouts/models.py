from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class WorkoutCategory(models.TextChoices):
    """
    Categories for workout plans
    """
    STRENGTH = 'ST', _('Strength Training')
    CARDIO = 'CD', _('Cardio')
    FLEXIBILITY = 'FL', _('Flexibility')
    HIIT = 'HI', _('High Intensity Interval Training')
    ENDURANCE = 'EN', _('Endurance')
    BALANCE = 'BL', _('Balance')
    YOGA = 'YG', _('Yoga')
    PILATES = 'PL', _('Pilates')
    CROSSFIT = 'CF', _('CrossFit')
    BODYWEIGHT = 'BW', _('Bodyweight')
    WEIGHTLIFTING = 'WL', _('Weightlifting')
    FUNCTIONAL = 'FN', _('Functional Training')
    OTHER = 'OT', _('Other')


class DifficultyLevel(models.TextChoices):
    """
    Difficulty levels for workout plans
    """
    BEGINNER = 'BG', _('Beginner')
    INTERMEDIATE = 'IM', _('Intermediate')
    ADVANCED = 'AD', _('Advanced')
    EXPERT = 'EX', _('Expert')


class BodyPart(models.TextChoices):
    """
    Body parts targeted by exercises
    """
    FULL_BODY = 'FB', _('Full Body')
    UPPER_BODY = 'UB', _('Upper Body')
    LOWER_BODY = 'LB', _('Lower Body')
    CORE = 'CR', _('Core')
    ARMS = 'AR', _('Arms')
    CHEST = 'CH', _('Chest')
    BACK = 'BK', _('Back')
    SHOULDERS = 'SH', _('Shoulders')
    LEGS = 'LG', _('Legs')
    GLUTES = 'GL', _('Glutes')
    CALVES = 'CV', _('Calves')
    BICEPS = 'BI', _('Biceps')
    TRICEPS = 'TR', _('Triceps')
    ABS = 'AB', _('Abs')


class Exercise(models.Model):
    """
    Model for individual exercises
    """
    name = models.CharField(_('Exercise Name'), max_length=200)
    description = models.TextField(_('Description'))
    body_part = models.CharField(
        _('Body Part'),
        max_length=2,
        choices=BodyPart.choices,
        default=BodyPart.FULL_BODY
    )
    difficulty = models.CharField(
        _('Difficulty'),
        max_length=2,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.BEGINNER
    )
    instructions = models.TextField(_('Instructions'))
    tips = models.TextField(_('Tips'), blank=True, null=True)
    image = models.ImageField(
        _('Exercise Image'),
        upload_to='workouts/exercises/',
        null=True,
        blank=True
    )
    video_url = models.URLField(
        _('Video URL'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('URL to a video demonstrating the exercise')
    )
    equipment_needed = models.BooleanField(_('Equipment Needed'), default=False)
    equipment_description = models.CharField(
        _('Equipment Description'),
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Exercise')
        verbose_name_plural = _('Exercises')
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    """
    Model for workout plans
    """
    name = models.CharField(_('Plan Name'), max_length=200)
    description = models.TextField(_('Description'))
    category = models.CharField(
        _('Category'),
        max_length=2,
        choices=WorkoutCategory.choices,
        default=WorkoutCategory.OTHER
    )
    difficulty = models.CharField(
        _('Difficulty'),
        max_length=2,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.BEGINNER
    )
    duration_weeks = models.PositiveIntegerField(_('Duration (weeks)'), default=4)
    sessions_per_week = models.PositiveIntegerField(_('Sessions per Week'), default=3)
    minutes_per_session = models.PositiveIntegerField(_('Minutes per Session'), default=30)
    goal = models.TextField(_('Goal'), blank=True, null=True)
    image = models.ImageField(
        _('Plan Image'),
        upload_to='workouts/plans/',
        null=True,
        blank=True
    )
    is_featured = models.BooleanField(_('Featured'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Workout Plan')
        verbose_name_plural = _('Workout Plans')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):
    """
    Model for days in a workout plan
    """
    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name='days'
    )
    day_number = models.PositiveIntegerField(_('Day Number'))
    name = models.CharField(_('Day Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    rest_day = models.BooleanField(_('Rest Day'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Workout Day')
        verbose_name_plural = _('Workout Days')
        ordering = ['workout_plan', 'day_number']
        unique_together = ['workout_plan', 'day_number']

    def __str__(self):
        return f"{self.workout_plan.name} - Day {self.day_number}: {self.name}"


class WorkoutExercise(models.Model):
    """
    Model for exercises in a workout day
    """
    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='workout_exercises'
    )
    order = models.PositiveIntegerField(_('Order'), default=1)
    sets = models.PositiveIntegerField(_('Sets'), default=3)
    reps = models.CharField(_('Reps'), max_length=50, default='10')
    rest_seconds = models.PositiveIntegerField(_('Rest (seconds)'), default=60)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Workout Exercise')
        verbose_name_plural = _('Workout Exercises')
        ordering = ['workout_day', 'order']
        unique_together = ['workout_day', 'exercise', 'order']

    def __str__(self):
        return f"{self.workout_day.name} - {self.exercise.name}"


class VideoTutorial(models.Model):
    """
    Model for video tutorials related to workout plans
    """
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    video_url = models.URLField(
        _('Video URL'),
        max_length=255,
        help_text=_('URL to the video tutorial (e.g., YouTube)')
    )
    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name='video_tutorials'
    )
    duration_minutes = models.PositiveIntegerField(_('Duration (minutes)'), default=0)
    duration_seconds = models.PositiveIntegerField(_('Duration (seconds)'), default=0)
    thumbnail = models.ImageField(
        _('Thumbnail'),
        upload_to='workouts/videos/thumbnails/',
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField(_('Order'), default=1)
    is_featured = models.BooleanField(_('Featured'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Video Tutorial')
        verbose_name_plural = _('Video Tutorials')
        ordering = ['workout_plan', 'order']
        unique_together = ['workout_plan', 'order']

    def __str__(self):
        return f"{self.workout_plan.name} - {self.title}"

    @property
    def get_duration_display(self):
        """Return formatted duration string (MM:SS)"""
        minutes = self.duration_minutes
        seconds = self.duration_seconds
        return f"{minutes}:{seconds:02d}"


class VideoCategory(models.TextChoices):
    """
    Categories for saved videos
    """
    WORKOUT = 'WO', _('Workout')
    NUTRITION = 'NU', _('Nutrition')
    MOTIVATION = 'MO', _('Motivation')
    TECHNIQUE = 'TE', _('Technique')
    STRETCHING = 'ST', _('Stretching')
    RECOVERY = 'RE', _('Recovery')
    OTHER = 'OT', _('Other')


class SavedVideo(models.Model):
    """
    Model for videos saved by users in their library
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_videos'
    )
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True, null=True)
    video_url = models.URLField(
        _('Video URL'),
        max_length=255,
        help_text=_('URL to the video (e.g., YouTube)')
    )
    category = models.CharField(
        _('Category'),
        max_length=2,
        choices=VideoCategory.choices,
        default=VideoCategory.OTHER
    )
    duration_minutes = models.PositiveIntegerField(_('Duration (minutes)'), default=0)
    duration_seconds = models.PositiveIntegerField(_('Duration (seconds)'), default=0)
    thumbnail = models.ImageField(
        _('Thumbnail'),
        upload_to='workouts/saved_videos/thumbnails/',
        null=True,
        blank=True
    )
    is_favorite = models.BooleanField(_('Favorite'), default=False)
    notes = models.TextField(_('Personal Notes'), blank=True, null=True)
    source_type = models.CharField(
        _('Source Type'),
        max_length=20,
        choices=[
            ('tutorial', _('Workout Tutorial')),
            ('external', _('External Video')),
            ('custom', _('Custom Upload'))
        ],
        default='external'
    )
    source_id = models.PositiveIntegerField(
        _('Source ID'),
        null=True,
        blank=True,
        help_text=_('ID of the source video if from a tutorial')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Saved Video')
        verbose_name_plural = _('Saved Videos')
        ordering = ['-created_at']
        unique_together = ['user', 'video_url']

    def __str__(self):
        return f"{self.user.name} - {self.title}"

    @property
    def get_duration_display(self):
        """Return formatted duration string (MM:SS)"""
        minutes = self.duration_minutes
        seconds = self.duration_seconds
        return f"{minutes}:{seconds:02d}"


class UserWorkout(models.Model):
    """
    Model for tracking user's selected workout plans
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workouts'
    )
    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name='user_workouts'
    )
    start_date = models.DateField(_('Start Date'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)
    completed = models.BooleanField(_('Completed'), default=False)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Workout')
        verbose_name_plural = _('User Workouts')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name} - {self.workout_plan.name}"
