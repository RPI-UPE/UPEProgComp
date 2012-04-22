import os
import mimetypes

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

from settings import USERS_URL

# Passed to FileField() to dynamically set resume filenames
def get_resume_path(instance, filename=None):
    resume = instance.resume.file
    extension = mimetypes.guess_extension(resume.content_type)
    return os.path.join('resumes',  # Save to the media/resumes/ directory
            instance.user.username + '_' + instance.first_name + instance.last_name + extension)

class Profile(models.Model):
    user   = models.OneToOneField(User, unique=True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    grad   = models.DateField()
    resume = models.FileField(upload_to=get_resume_path, blank=True)

    def __str__(self):
        return str(self.user)

    def _get_resume_path(self):
        return USERS_URL + os.path.basename(self.resume.name)
    resume_url = property(_get_resume_path)


is_registered = user_passes_test(lambda u:
        u.is_authenticated() and
        Profile.objects.filter(user=u.pk).count() > 0)

is_staff = user_passes_test(lambda u:
        u.is_authenticated() and u.is_staff)
