import collections
from django.db import models

from progcomp.account.models import Profile
from progcomp.submission.models import Submission


class Scoreboard(models.Model):
    def __str__(self):
        return 'Top Submissions'
