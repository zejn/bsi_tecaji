
from django import forms

class TecajForm(forms.Form):
    datum = forms.DateField(required=True)
    oznaka = forms.CharField(required=False)

    def clean(self):
        d = self.cleaned_data
        if not d['oznaka']:
            del d['oznaka']
        return d