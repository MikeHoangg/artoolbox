from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArtoolboxAuthConfig(AppConfig):
    name = 'apps.artoolbox_auth'
    verbose_name = _('Authorization')
