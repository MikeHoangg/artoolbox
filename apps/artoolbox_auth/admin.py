from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.artoolbox_auth.models import ArtoolboxUser

admin.site.register(ArtoolboxUser, UserAdmin)
