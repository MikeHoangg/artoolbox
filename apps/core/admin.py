from django.contrib import admin

from apps.core.models import Image, Tool, Material
from apps.core.utils import colours


class ToolAdmin(admin.ModelAdmin):
    filter_horizontal = ('materials',)


class ImageAdmin(admin.ModelAdmin):
    filter_horizontal = ('tools',)
    readonly_fields = ('colours',)

    def save_model(self, request, obj, form, change):
        obj.colours = list(colours(obj.file.open(), 4))
        super(ImageAdmin, self).save_model(request, obj, form, change)


admin.site.register(Material)
admin.site.register(Tool, ToolAdmin)
admin.site.register(Image, ImageAdmin)
