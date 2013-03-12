import os

from django.db import models
from django.conf import settings

from progcomp.submission.models import Submission
from progcomp.utils import user_upload

class Result(models.Model):
    submission  = models.OneToOneField(Submission)
    status      = models.CharField(max_length=32)
    created     = models.DateTimeField(auto_now_add=True)
    diff        = models.FileField(upload_to=user_upload('diff',
                    lambda i: str(i.submission.id)), blank=True)
