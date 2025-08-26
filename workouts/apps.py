from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WorkoutsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workouts'
    verbose_name = _('Workouts')
