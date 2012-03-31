import collections
from django.db import models

from progcomp.account.models import Profile
from progcomp.submission.models import Submission


class Scoreboard(models.Model):

    def __str__(self):
        return 'Top Submissions'

    def users(self):
        valid_submissions = Submission.objects.all() \
                .filter(result__status='success') \
                .values_list('registrant', 'attempt__problem', 'submitted') \
                .distinct()
        users = collections.defaultdict(dict)
        for user, problem, dt in list(valid_submissions):
            if problem in users[user] and users[user][problem] > dt:
                users[user][problem] = dt
            elif problem not in users[user]:
                users[user][problem] = dt
        ranks = []
        for user, problems in users.items():
            number_submitted = len(problems.keys())
            max_time = max(problems.values())
            ranks.append( (number_submitted, max_time, user) )
        def comp(lhs, rhs):
            if lhs[0] > rhs[0]:
                return -1
            elif lhs[0] == rhs[0]:
                return cmp(lhs[1], rhs[1])
            else:
                return 1
        ranks.sort(comp)
        users = Profile.objects.in_bulk(map(lambda x: x[2], ranks))
        return map(lambda y: (users[y[2]].user, y[0], y[1]), ranks)
