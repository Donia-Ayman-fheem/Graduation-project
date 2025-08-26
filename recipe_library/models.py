from django.db import models
from django.utils.translation import gettext_lazy as _


class RecipeCategory(models.TextChoices):
    """
    Categories for recipes
    """
    BREAKFAST = 'BF', _('Breakfast')
    LUNCH = 'LN', _('Lunch')
    DINNER = 'DN', _('Dinner')
    SNACK = 'SN', _('Snack')
    DESSERT = 'DS', _('Dessert')
    BEVERAGE = 'BV', _('Beverage')
    VEGETARIAN = 'VG', _('Vegetarian')
    VEGAN = 'VN', _('Vegan')
    KETO = 'KT', _('Keto')
    LOW_CARB = 'LC', _('Low Carb')
    HIGH_PROTEIN = 'HP', _('High Protein')
    OTHER = 'OT', _('Other')


class Recipe(models.Model):
    """
    Model for recipes in the recipe library
    """
    title = models.CharField(_('Recipe Title'), max_length=200)
    description = models.TextField(_('Description'))
    category = models.CharField(
        _('Category'),
        max_length=2,
        choices=RecipeCategory.choices,
        default=RecipeCategory.OTHER
    )
    ingredients = models.TextField(_('Ingredients'))
    instructions = models.TextField(_('Instructions'))
    preparation_time = models.PositiveIntegerField(
        _('Preparation Time (minutes)'),
        null=True,
        blank=True
    )
    cooking_time = models.PositiveIntegerField(
        _('Cooking Time (minutes)'),
        null=True,
        blank=True
    )
    servings = models.PositiveIntegerField(_('Servings'), null=True, blank=True)
    calories = models.PositiveIntegerField(_('Calories per Serving'), null=True, blank=True)
    protein = models.DecimalField(
        _('Protein (g)'),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True
    )
    carbs = models.DecimalField(
        _('Carbs (g)'),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True
    )
    fat = models.DecimalField(
        _('Fat (g)'),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True
    )
    image = models.ImageField(
        _('Recipe Image'),
        upload_to='recipes/images/',
        null=True,
        blank=True
    )
    video_url = models.URLField(
        _('Video URL'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('URL to a video of the recipe (e.g., YouTube)')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
