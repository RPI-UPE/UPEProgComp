from django import forms

from progcomp.judge.models import Grading
from progcomp.judge.models import Result


choices = ['SERVERERROR', 'COMPILEERROR', 'RUNERROR', 'TIMEERROR', 'SPACEERROR', 'OUTPUTERROR', 'SUCCESS']
choices_map = zip(choices, choices)


class ResultForm(forms.Form):

    nonce       = forms.CharField(max_length=128)
    status      = forms.ChoiceField(choices=choices_map)
    compilecode = forms.IntegerField(required=False)
    runcode     = forms.IntegerField(required=False)
    runtime     = forms.IntegerField(required=False)

    def clean(self):
        cleaned = self.cleaned_data

        if 'nonce' not in cleaned:
            raise forms.ValidationError('No nonce')
        try:
            grading = Grading.objects.get(nonce=cleaned['nonce'])
        except:
            raise forms.ValidationError('Error fetching Grading')
        cleaned['grading'] = grading
        return cleaned
