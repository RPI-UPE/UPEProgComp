import datetime
import os
import random
from contextlib import contextmanager

from django.db import models
from django.conf import settings

from progcomp.account.models import Profile
from progcomp.problems.models import Problem

class Attempt(models.Model):
    person = models.ForeignKey(Profile)
    problem = models.ForeignKey(Problem)
    startTime = models.DateTimeField(auto_now_add=True)
    input_id = models.IntegerField()

    def __str__(self):
        return "%s %s %s"%(str(self.person),str(self.problem),str(self.startTime))

    @staticmethod
    def create(user, problem_id):
        new = Attempt( person = user.profile,
                       startTime = datetime.datetime.now())
        try:
            new.problem = Problem.objects.get(pk=problem_id)
            new.input_id = new.create_input()
        except Problem.DoesNotExist:
            raise Exception("Invalid problem id")

        return new

    def time_since(self):
        timediff = datetime.datetime.now() - self.startTime
        return (timediff.microseconds + (timediff.seconds + timediff.days * 24 * 3600) * 10**6) / 10**6

    def create_input(self):
        selected_number = random.randint(0, self.problem.available_inputs - 1)
        target_symlink = os.path.join(settings.MEDIA_ROOT,
                                      self.person.user_directory('input'),
                                      self.problem.slug+'.in')

        link_name = os.path.join(self.problem.path, '%d.in' % selected_number)

        if (os.path.lexists(target_symlink)):
            os.unlink(target_symlink)

        os.link(link_name, target_symlink)

        return selected_number

    @property
    @contextmanager
    def expected_output_file(self):
        with self.problem.exepected_output_file(self.input_id) as f:
            yield f
        
class Submission(models.Model):
    registrant = models.ForeignKey(Profile)
    attempt = models.ForeignKey(Attempt)
    submitted  = models.DateTimeField(auto_now_add=True)
    sourcecode = models.FileField(upload_to=lambda i,f: \
                    os.path.join(i.registrant.user_directory('source'), f))
    output_file = models.FileField(upload_to=lambda i,f: \
                    os.path.join(i.registrant.user_directory('output'), f))

    def __str__(self):
        return '%s:%s' % (str(self.registrant), str(self.attempt.problem))

    @staticmethod
    def user_summary(user):
        return Submission.objects \
                    .select_related('attempt', 'attempt__problem', 'result') \
                    .filter(registrant__user=user) \
                    .order_by('submitted').reverse()

    @property
    @contextmanager
    def user_output_file(self):
        with open(self.output_file.path) as f:
            yield f
