import os

from django.db import models

from progcomp.file_creation_utils import user_directory
from progcomp.submission.models import Submission

class Result(models.Model):
    submission  = models.OneToOneField(Submission)
    status      = models.CharField(max_length=16)
    created     = models.DateTimeField(auto_now_add=True)
    diff        = models.FileField(upload_to=lambda x,f=None: os.path.join(user_directory(x.submission.registrant.user.username, 'diff'), str(x.submission.id)),
                                    blank=True)
