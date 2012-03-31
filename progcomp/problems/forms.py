from django import forms

from progcomp.problems.models import Problem


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
