from django import forms
from .utils import colours


class AnalyseForm(forms.Form):
    file = forms.FileField(required=True, allow_empty_file=False)

    def get_analysis_result(self):
        file = self.cleaned_data['file']
        return list(colours(file, 4))

    class Meta:
        widgets = {
            'page_1': forms.FileInput(attrs={'accept': 'image/*'})
        }
