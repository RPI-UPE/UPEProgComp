import os

from django.db import models
from django.conf import settings

from progcomp.submission.models import Submission

class Result(models.Model):
    submission  = models.OneToOneField(Submission)
    status      = models.CharField(max_length=32)
    created     = models.DateTimeField(auto_now_add=True)
    diff        = models.FileField(upload_to=lambda x,f=None: os.path.join(settings.MEDIA_ROOT,
                        x.submission.registrant.user_directory('diff'), str(x.submission.id)),
                        blank=True)
