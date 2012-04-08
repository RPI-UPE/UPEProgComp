import collections
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from progcomp.account.models import Profile
from progcomp.submission.models import Submission
from progcomp.problems.models import Problem


@login_required
def scoreboard(request, template='scoreboard/scoreboard.html'):
    context = {}

    # Get all submissions
    valid_submissions = Submission.objects.all() \
            .filter(result__status='success') \
            .values_list('registrant', 'attempt__problem', 'submitted') \
            .distinct()

    # Get problem set for size count and names
    problem_set = Problem.objects.all()

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
        ranks.append( (number_submitted, max_time, user) )
    def comp(lhs, rhs):
        if lhs[0] == rhs[0]:
            return cmp(lhs[1], rhs[1])
        return -cmp(lhs[0], rhs[0])
    ranks.sort(comp)

    # Given a user id, return a list of times said user completed each 
    # problem, or None in place if user has not yet completed
    def user_solns(user):
        # Store solution as a list with incomplete being None
        solns = users[user]
        solns = [i in solns and solns[i] or None for i in range(1, len(problem_set)+1)]
        # Map to relative time
        solns = map(lambda y: y and (y - settings.START).seconds, solns)
        return map(lambda y: y and "%d:%02d:%02d" % (y/3600, (y/60)%60, y%60), solns)

    # Get information (fname, lname) for each user, map user object over id
    profiles = Profile.objects.in_bulk(map(lambda x: x[2], ranks))
    context['scoreboard'] = map(lambda y: (profiles[y[2]].user, y[0], y[1], user_solns(y[2])), ranks)
    context['is_ended'] = datetime.datetime.now() > settings.END
    context['problems'] = problem_set
    return render_to_response(template, context,
            context_instance=RequestContext(request))
