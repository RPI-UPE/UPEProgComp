import os
import mimetypes

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

from progcomp.utils import user_upload

class Profile(models.Model):
    user   = models.OneToOneField(User, unique=True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    grad   = models.DateField()
    resume = models.FileField(blank=True, upload_to=user_upload('',
                lambda i: 'resume' + mimetypes.guess_extension(i.resume.file.content_type)))

    def __str__(self):
        return str(self.user)

    @property
    def resume_url(self):
        return settings.USERS_URL + os.path.basename(self.resume.name)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def token(self):
        # Remove all spaces, periods, and slashes
        name = reduce(lambda acc, i: acc.replace(i, ''), [' ', '.', '/'], self.full_name)
        return '%s_%d' % (name, self.pk)

    def user_directory(self, subdir=''):
        # Path is relative to media root so that Django's upload_to can handle it
        path = os.path.relpath(os.path.join(settings.USERS_ROOT, self.token),  settings.MEDIA_ROOT)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

is_registered = user_passes_test(lambda u:
        u.is_authenticated() and
        Profile.objects.filter(user=u.pk).count() > 0)

is_staff = user_passes_test(lambda u:
        u.is_authenticated() and u.is_staff)
