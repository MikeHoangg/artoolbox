import requests
from django import forms

from apps.core.models import Tool
from .utils import colours, get_tools_by_colours
from django.conf import settings


class AnalyseForm(forms.Form):
    file = forms.FileField(required=True, allow_empty_file=False)

    def get_analysis_result(self):
        file = self.cleaned_data['file']
        dominating_colours = colours(file)
        response = requests.post(
            "http://{}:{}/v1/models/{}:predict".format(
                settings.TENSORFLOW_HOST, settings.TENSORFLOW_PORT, settings.TENSORFLOW_MODEL
            )
        )
        if response.status_code == 200:
            recommended_tools_ids = response.json()['prediction']
            recommended_tools = Tool.objects.filter(id__in=recommended_tools_ids).prefetch_related('materials')
        else:
            recommended_tools = get_tools_by_colours(dominating_colours).prefetch_related('materials')
        return dominating_colours, recommended_tools

    class Meta:
        widgets = {
            'page_1': forms.FileInput(attrs={'accept': 'image/*'})
        }
