from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DietPlansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diet_plans'
    verbose_name = _('Diet Plans')
