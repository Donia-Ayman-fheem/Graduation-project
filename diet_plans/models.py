from django.db import models
from django.utils.translation import gettext_lazy as _


class DietPlanCategory(models.TextChoices):
    """
    Categories for diet plans
    """
    WEIGHT_LOSS = 'WL', _('Weight Loss')
    MUSCLE_GAIN = 'MG', _('Muscle Gain')
    MAINTENANCE = 'MT', _('Maintenance')
    VEGETARIAN = 'VG', _('Vegetarian')
    VEGAN = 'VN', _('Vegan')
    KETO = 'KT', _('Keto')
    LOW_CARB = 'LC', _('Low Carb')
    HIGH_PROTEIN = 'HP', _('High Protein')
    BALANCED = 'BL', _('Balanced')


class MealType(models.TextChoices):
    """
    Types of meals in a diet plan
    """
    BREAKFAST = 'BF', _('Breakfast')
    LUNCH = 'LN', _('Lunch')
    DINNER = 'DN', _('Dinner')
    SNACK = 'SN', _('Snack')
    PRE_WORKOUT = 'PW', _('Pre-Workout')
    POST_WORKOUT = 'PT', _('Post-Workout')


class DietPlan(models.Model):
    """
    Model for diet plans
    """
    name = models.CharField(_('Plan Name'), max_length=100)
    description = models.TextField(_('Description'))
    category = models.CharField(
        _('Category'),
        max_length=2,
        choices=DietPlanCategory.choices,
        default=DietPlanCategory.BALANCED
    )
    duration_weeks = models.PositiveIntegerField(_('Duration (weeks)'), default=4)
    calories_per_day = models.PositiveIntegerField(_('Calories per Day'), null=True, blank=True)
    protein_percentage = models.PositiveIntegerField(_('Protein %'), null=True, blank=True)
    carbs_percentage = models.PositiveIntegerField(_('Carbs %'), null=True, blank=True)
    fat_percentage = models.PositiveIntegerField(_('Fat %'), null=True, blank=True)
    image = models.ImageField(_('Plan Image'), upload_to='diet_plans/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Diet Plan')
        verbose_name_plural = _('Diet Plans')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"


class DietPlanWeek(models.Model):
    """
    Model for organizing diet plans by weeks
    """
    diet_plan = models.ForeignKey(
        DietPlan,
        on_delete=models.CASCADE,
        related_name='weeks'
    )
    week_number = models.PositiveIntegerField(_('Week Number'))
    description = models.TextField(_('Week Description'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Diet Plan Week')
        verbose_name_plural = _('Diet Plan Weeks')
        ordering = ['diet_plan', 'week_number']
        unique_together = ['diet_plan', 'week_number']

    def __str__(self):
        return f"{self.diet_plan.name} - Week {self.week_number}"


class DietPlanMeal(models.Model):
    """
    Model for individual meals within a diet plan week
    """
    week = models.ForeignKey(
        DietPlanWeek,
        on_delete=models.CASCADE,
        related_name='meals'
    )
    day_of_week = models.PositiveIntegerField(
        _('Day of Week'),
        choices=[(1, _('Monday')), (2, _('Tuesday')), (3, _('Wednesday')),
                (4, _('Thursday')), (5, _('Friday')), (6, _('Saturday')),
                (7, _('Sunday'))]
    )
    meal_type = models.CharField(
        _('Meal Type'),
        max_length=2,
        choices=MealType.choices
    )
    name = models.CharField(_('Meal Name'), max_length=100)
    description = models.TextField(_('Meal Description'))
    ingredients = models.TextField(_('Ingredients'))
    preparation = models.TextField(_('Preparation Instructions'), null=True, blank=True)
    calories = models.PositiveIntegerField(_('Calories'), null=True, blank=True)
    protein = models.DecimalField(_('Protein (g)'), max_digits=5, decimal_places=1, null=True, blank=True)
    carbs = models.DecimalField(_('Carbs (g)'), max_digits=5, decimal_places=1, null=True, blank=True)
    fat = models.DecimalField(_('Fat (g)'), max_digits=5, decimal_places=1, null=True, blank=True)
    image = models.ImageField(_('Meal Image'), upload_to='diet_plans/meals/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Diet Plan Meal')
        verbose_name_plural = _('Diet Plan Meals')
        ordering = ['week', 'day_of_week', 'meal_type']
        unique_together = ['week', 'day_of_week', 'meal_type']

    def __str__(self):
        return f"{self.week.diet_plan.name} - Week {self.week.week_number} - Day {self.day_of_week} - {self.get_meal_type_display()}"
