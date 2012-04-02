import collections
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from progcomp.account.models import Profile
from progcomp.submission.models import Submission


@login_required
def scoreboard(request, template='scoreboard/scoreboard.html'):
    context = {}

    # Get all submissions
    valid_submissions = Submission.objects.all() \
            .filter(result__status='success') \
            .values_list('registrant', 'attempt__problem', 'submitted') \
            .distinct()

    # Build dictionary of users mapped to problems mapped to time completed
    users = collections.defaultdict(dict)
    for user, problem, dt in list(valid_submissions):
        if problem not in users[user] or users[user][problem] > dt:
            users[user][problem] = dt

    # Summarize dict for sorting by rank (num_correct, latest_time, user)
    ranks = []
    for user, problems in users.items():
        number_submitted = len(problems.keys())
        max_time = max(problems.values())
        diff_time = (max_time - settings.START).seconds
        time_fmt = "%d:%02d:%02d" % (diff_time/3600, (diff_time/60)%60, diff_time%60)
        ranks.append( (number_submitted, time_fmt, user) )
    def comp(lhs, rhs):
        if lhs[0] == rhs[0]:
            return cmp(lhs[1], rhs[1])
        return cmp(lhs[0], rhs[0])
    ranks.sort(comp)

    # Get information (fname, lname) for each user, map user object over id
    users = Profile.objects.in_bulk(map(lambda x: x[2], ranks))
    context['scoreboard'] = map(lambda y: (users[y[2]].user, y[0], y[1]), ranks)
    context['is_ended'] = datetime.datetime.now() > settings.END
    return render_to_response(template, context,
            context_instance=RequestContext(request))
