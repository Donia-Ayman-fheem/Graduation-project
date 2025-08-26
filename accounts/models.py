from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from diet_plans.models import DietPlan
from workouts.models import WorkoutPlan

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, name, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

# Gender choices
class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    OTHER = 'O', _('Other')
    PREFER_NOT_TO_SAY = 'N', _('Prefer not to say')

# Fitness goals choices
class FitnessGoal(models.TextChoices):
    WEIGHT_LOSS = 'WL', _('Weight Loss')
    MUSCLE_GAIN = 'MG', _('Muscle Gain')
    ENDURANCE = 'EN', _('Endurance')
    FLEXIBILITY = 'FL', _('Flexibility')
    GENERAL_FITNESS = 'GF', _('General Fitness')
    STRENGTH = 'ST', _('Strength')
    OTHER = 'OT', _('Other')

# User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.PREFER_NOT_TO_SAY
    )
    fitness_goal = models.CharField(
        max_length=2,
        choices=FitnessGoal.choices,
        default=FitnessGoal.GENERAL_FITNESS
    )
    diet_plan = models.ForeignKey(
        DietPlan,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True,
        verbose_name=_('Selected Diet Plan')
    )
    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.SET_NULL,
        related_name='profile_users',
        null=True,
        blank=True,
        verbose_name=_('Selected Workout Plan')
    )
    # Body measurements
    height = models.DecimalField(
        _('Height (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    weight = models.DecimalField(
        _('Weight (kg)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    waist_circumference = models.DecimalField(
        _('Waist Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    hip_circumference = models.DecimalField(
        _('Hip Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    chest_circumference = models.DecimalField(
        _('Chest Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    arm_circumference = models.DecimalField(
        _('Arm Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    thigh_circumference = models.DecimalField(
        _('Thigh Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    neck_circumference = models.DecimalField(
        _('Neck Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    body_photo = models.ImageField(
        _('Full-body Photo'),
        upload_to='body_measurements/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name}'s Profile"
