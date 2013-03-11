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
            new.inputCases = new.create_input()
        except Problem.DoesNotExist:
            raise Exception("Invalid problem id")

        return new

    def time_since(self):
        timediff = datetime.datetime.now() - self.startTime
        return (timediff.microseconds + (timediff.seconds + timediff.days * 24 * 3600) * 10**6) / 10**6

    def create_input(self):
        # TODO refactor number_in_problem
        problem_path = os.path.join(settings.GRADE_DIR, self.problem.slug)
        if(os.path.exists(problem_path)):
            selected_number = random.randint(0, self.problem.number_in_problem-1)
            target_symlink = os.path.join(self.person.user_directory('input'), self.problem.slug+'.in')

            link_name = os.path.join(problem_path, str(selected_number)+'.in')

            logging.info('%s --> %s'%(link_name, target_symlink))

            if (os.path.lexists(target_symlink)):
                os.unlink(target_symlink)

            os.link(link_name, target_symlink)

            return selected_number
        else:
            raise Exception('Invalid Problem Name')
        
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
