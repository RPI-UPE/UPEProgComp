import datetime
import mimetypes
import os
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from file_creation_utils import user_grade_dir_name

from progcomp.account.models import Profile
from progcomp.utils import handle_upload_file


grad_dates = map(lambda x: (x, x.strftime('%Y-%m')), settings.GRAD_DATES)


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(required = True, max_length = 20)
    last_name = forms.CharField(required = True, max_length = 20)
    email  = forms.EmailField(required = True)
    
    grad   = forms.ChoiceField(choices = grad_dates, required=True)
    resume = forms.FileField(required = False)

    def save(self, commit=True):
        if not commit:
            raise ValueError("Must commit the registration form")
        user = super(RegistrationForm, self).save(commit=True)
        user.email = self.cleaned_data['email']
        user.save()

        grad = self.cleaned_data['grad']
        profile, new = Profile.objects.get_or_create(user=user, grad=grad)
        udir = os.path.join(settings.MEDIA_ROOT, 'resumes/')
        resume = self.cleaned_data['resume']

        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']
        
        user.first_name = profile.first_name;
        user.last_name = profile.last_name;
        user.save()

        if resume is not None:
            path = handle_upload_file(resume, user.username, profile.first_name, profile.last_name, udir)
            profile.resume = path[len(settings.MEDIA_ROOT):]
        profile.save()

        dir_name = settings.USERS_ROOT + user_grade_dir_name(user.username)
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

        return user

    def clean_grad(self):
        d = self.cleaned_data['grad']
        return datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')

    def clean_resume(self):
        r = self.cleaned_data['resume']
        if r is None:
            return None
        if mimetypes.guess_extension(r.content_type) is None:
            raise forms.ValidationError('Unknown mimetype for resume; try PDF or TXT')
        if r.content_type not in settings.RESUME_TYPES:
            raise forms.ValidationError('Invalid mimetype for resume; try %s' %
                (' or '.join(settings.RESUME_TYPES)))
        return r


class AdminForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)


class ProfileForm(forms.ModelForm):

    grad   = forms.ChoiceField(choices=grad_dates, required=True)

    class Meta:
        model = Profile
        exclude = ('user',)

    def clean_grad(self):
        d = self.cleaned_data['grad']
        return datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')

    def clean_resume(self):
        r = self.cleaned_data['resume']
        if r is None:
            return None
        if mimetypes.guess_extension(r.content_type) is None:
            raise forms.ValidationError('Unknown mimetype for resume; try PDF or TXT')
        if r.content_type not in settings.RESUME_TYPES:
            raise forms.ValidationError('Invalid mimetype for resume; try %s' %
                (' or '.join(settings.RESUME_TYPES)))
        return r
