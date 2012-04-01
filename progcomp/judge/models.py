from django.db import models
from django.contrib.auth.models import User

from progcomp.submission.models import Submission


class Grading(models.Model):
    submission = models.OneToOneField(Submission)
    grader     = models.ForeignKey(User)
    nonce      = models.CharField(max_length=128, unique=True)
    requested  = models.DateTimeField(auto_now_add=True)


class Result(models.Model):
    submission  = models.OneToOneField(Submission)
    status      = models.CharField(max_length=16)
    created     = models.DateTimeField(auto_now_add=True)
    diff        = models.FileField(upload_to='diffs/',blank=True)
