import mimetypes
from django import forms
from django.forms.util import ErrorList

from progcomp.submission.models import Submission
from progcomp.problems.models import Problem


class SubmissionForm(forms.ModelForm):

    #problem = forms.ModelChoiceField(queryset=Problem.objects.all(),
    #        widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Submission
        exclude = ('registrant','attempt','problem')

    def clean(self):
        cleaned = self.cleaned_data
        if 'sourcecode' not in cleaned:
            return cleaned

        return cleaned

    def save(self, commit=True):
        s = super(SubmissionForm, self).save(commit)
        return s
