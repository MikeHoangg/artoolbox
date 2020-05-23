from admin_interface.models import Theme
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.unregister(Theme)
