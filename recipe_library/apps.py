from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecipeLibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipe_library'
    verbose_name = _('Recipe Library')
