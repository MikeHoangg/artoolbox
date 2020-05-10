from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class ArtoolboxUser(AbstractUser):
    """
    User model
    """
    email = models.EmailField(_('email address'))

    def __str__(self):
        return self.username
