import os

from django.db import models
from django.conf import settings

from progcomp.submission.models import Submission

class Result(models.Model):
    submission  = models.OneToOneField(Submission)
    status      = models.CharField(max_length=32)
    created     = models.DateTimeField(auto_now_add=True)
    diff        = models.FileField(blank=True, upload_to=lambda i,f: \
                    os.path.join(i.submission.registrant.user_directory('diff'), f))
