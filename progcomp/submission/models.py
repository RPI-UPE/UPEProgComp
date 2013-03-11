import datetime

from django.db import models

from progcomp.account.models import Profile
from progcomp.problems.models import Problem

class Attempt(models.Model):
    person = models.ForeignKey(Profile)
    problem = models.ForeignKey(Problem)
    startTime = models.DateTimeField(auto_now_add=True)
    inputCases = models.IntegerField()

    def __str__(self):
        return "%s %s %s"%(str(self.person),str(self.problem),str(self.startTime))

    @staticmethod
    def create(user, problem_id):
        new = Attempt( person = user.profile,
                       startTime = datetime.datetime.now())
        try:
            new.problem = Problem.objects.get(pk=problem_id)
            new.inputCases = create_test_input(new.problem.slug, user.profile, new.problem.number_in_problem)
        except Problem.DoesNotExist:
            raise Exception("Invalid problem id")

        return new

    def time_since(self):
        timediff = datetime.datetime.now() - self.startTime
        return (timediff.microseconds + (timediff.seconds + timediff.days * 24 * 3600) * 10**6) / 10**6
        
class Submission(models.Model):
    registrant = models.ForeignKey(Profile)
    attempt = models.ForeignKey(Attempt)
    submitted  = models.DateTimeField(auto_now_add=True)
    sourcecode = models.FileField(upload_to='sources/')
    output_file = models.FileField(upload_to='output_file/')

    def __str__(self):
        return '%s:%s' % (str(self.registrant), str(self.attempt.problem))

    @staticmethod
    def user_summary(user):
        return Submission.objects \
                    .select_related('attempt', 'attempt__problem', 'result') \
                    .filter(registrant__user=user) \
                    .order_by('submitted').reverse()
