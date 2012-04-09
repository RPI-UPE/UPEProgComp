from django import forms

from progcomp.submission.models import Submission

class SubmissionForm(forms.ModelForm):

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
