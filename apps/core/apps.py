from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = 'apps.core'
    verbose_name = _("Artoolbox")
