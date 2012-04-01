from django.db import models
from progcomp.submission.models import Submission


class Result(models.Model):
    submission  = models.OneToOneField(Submission)
    status      = models.CharField(max_length=16)
    created     = models.DateTimeField(auto_now_add=True)
    diff        = models.FileField(upload_to='diffs/',blank=True)
