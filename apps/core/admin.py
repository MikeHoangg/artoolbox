import re

from django.contrib import admin

from apps.core.models import Image, Tool, Material
from apps.core.utils import colours


class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


class ToolAdmin(admin.ModelAdmin):
    REVERSED_TYPE_CHOICES = {choice[1]: choice[0] for choice in Tool.TYPE_CHOICES}

    search_fields = ('name', 'tool_type')
    filter_horizontal = ('materials',)
    list_display = ('name', 'tool_type')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ToolAdmin, self).get_search_results(request, queryset, search_term)
        for key in self.REVERSED_TYPE_CHOICES.keys():
            if re.search(search_term, key, re.IGNORECASE):
                queryset |= self.model.objects.filter(tool_type=self.REVERSED_TYPE_CHOICES[key])
        return queryset, use_distinct


class ImageAdmin(admin.ModelAdmin):
    search_fields = ('name', 'artist', 'user__username')
    filter_horizontal = ('tools',)
    readonly_fields = ('colours',)
    list_display = ('name', 'artist', 'user')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        if 'file' in form.changed_data:
            obj.colours = list(colours(obj.file.open()))
        super(ImageAdmin, self).save_model(request, obj, form, change)


admin.site.register(Material, MaterialAdmin)
admin.site.register(Tool, ToolAdmin)
admin.site.register(Image, ImageAdmin)
