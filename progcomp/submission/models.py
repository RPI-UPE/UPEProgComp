from django.db import models
from django.conf import settings

from progcomp.account.models import Profile
from progcomp.problems.models import Problem

class Attempt(models.Model):
    person = models.ForeignKey(Profile)
    problem = models.ForeignKey(Problem)
    startTime = models.DateTimeField(auto_now_add=True)
    inputCases = models.IntegerField()

    def __str__(self):
        return "%s %s %s"%(str(self.person),str(self.problem),str(self.startTime))
        
class Submission(models.Model):

    registrant = models.ForeignKey(Profile)
    attempt = models.ForeignKey(Attempt)
    submitted  = models.DateTimeField(auto_now_add=True)
    sourcecode = models.FileField(upload_to='sources/')
    output_file = models.FileField(upload_to='output_file/')

    def __str__(self):
        return '%s:%s' % (str(self.registrant), str(self.attempt.problem))

