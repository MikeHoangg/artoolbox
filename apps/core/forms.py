import requests
from django import forms

from apps.core.models import Tool
from .utils import colours, get_tools_by_colours
from django.conf import settings


class AnalyseForm(forms.Form):
    file = forms.FileField(required=True, allow_empty_file=False)

    def get_analysis_result(self):
        file = self.cleaned_data['file']
        dominating_colours = sorted(list(colours(file)))

        # recommended_tools = self.get_results_from_tensor_flow(dominating_colours)
        recommended_tools = self.get_results_from_utils(dominating_colours)
        return dominating_colours, recommended_tools

    @staticmethod
    def get_results_from_tensor_flow(colours):
        """
        Function for getting recommended tools from tensorflow
        :param colours: list, of hex colours
        :return: QuerySet, of tools
        """
        data = {
            'instances': colours
        }
        response = requests.post(
            "http://{}:{}/v1/models/{}:predict".format(
                settings.TENSORFLOW_HOST, settings.TENSORFLOW_PORT, settings.TENSORFLOW_MODEL
            ),
            data
        )
        recommended_tools_ids = response.json()['prediction']
        return Tool.objects.filter(id__in=recommended_tools_ids).prefetch_related('materials')

    @staticmethod
    def get_results_from_utils(colours):
        """
        Function for getting recommended tools from utils
        :param colours: list, of hex colours
        :return: QuerySet, of tools
        """
        tools = get_tools_by_colours(colours)

        return tools.prefetch_related('materials')

    class Meta:
        widgets = {
            'page_1': forms.FileInput(attrs={'accept': 'image/*'})
        }
