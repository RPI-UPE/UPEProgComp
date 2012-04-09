import datetime
import mimetypes
import os
import itertools

from django import forms
from django.forms.widgets import FileInput
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from progcomp.account.models import Profile

grad_dates = map(lambda x: (x, x.strftime('%Y-%m')), settings.GRAD_DATES)

# Profile form for adding or updating profile-specific entitites
class ProfileForm(forms.ModelForm):
    grad   = forms.ChoiceField(choices = grad_dates, required=True)

    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {'resume': FileInput()}

    # Convert text into date
    def clean_grad(self):
        d = self.cleaned_data['grad']
        return datetime.datetime.strptime(d, '%Y-%m-%d').date()

    # We will clean resume here since we need to get instance information
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        resume = cleaned_data['resume']

        # Validate if a new resume was uploaded (InMemoryFile vs FieldFile)
        if resume and type(resume) != type(self.instance.resume):
            # MIME type error checking
            if mimetypes.guess_extension(resume.content_type) is None:
                raise forms.ValidationError('Unknown mimetype for resume; try PDF or TXT')
            if resume.content_type not in settings.RESUME_TYPES:
                raise forms.ValidationError('Invalid mimetype for resume; try %s' %
                    (' or '.join(settings.RESUME_TYPES)))

        return cleaned_data

    def save(self, commit=True):
        # If we already have a resume, remove it so that we don't keep storing copies
        resume = self.cleaned_data['resume']
        if resume and type(resume) != type(self.instance.resume):
            # Get filename directly from the method that FieldFile.save() will
            filename = self.instance.resume.field.generate_filename(self.instance)
            path = os.path.join(settings.MEDIA_ROOT, filename)
            if os.path.exists(path):
                os.remove(path)

        super(ProfileForm, self).save()


# Registration form inherits from Django base user form and keeps track of its
# own ProfileForm internally at the same time
class RegistrationForm(UserCreationForm):
    email  = forms.EmailField(required = True)

    # Setup our instance of profile to be made using all the same POST/FILE params
    def __init__(self, *args, **kwargs):
        self.profile = ProfileForm(*args, **kwargs)
        super(RegistrationForm, self).__init__(*args, **kwargs)

    # We want the form to show fields from both forms, so chain the iterators
    # together for the templater
    def __iter__(self):
        return itertools.chain(
            super(RegistrationForm, self).__iter__(),
            self.profile.__iter__()
        )

    def is_valid(self):
        return super(RegistrationForm, self).is_valid() and self.profile.is_valid()

    def save(self, commit=True):
        if not commit:
            raise ValueError("Must commit the registration form")

        # First commit the user
        self.instance.email = self.cleaned_data['email']
        user = super(RegistrationForm, self).save(commit=True)
        # Link the user to the profile and commit that
        self.profile.instance.user = user
        self.profile.save(commit=True)

        return user

class AdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
