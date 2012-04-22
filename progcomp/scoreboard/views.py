import datetime

from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from progcomp.account.models import Profile
from progcomp.scoreboard.models import Scoreboard
from progcomp.account.models import is_staff

@login_required
def scoreboard(request, template='scoreboard/scoreboard.html'):
    # Check the cache for a response object and return that if set. We're not
    # using Django's view/template cacher because we cannot invalidate them.
    sb_cache = cache.get('scoreboard')
    if sb_cache:
        return sb_cache

    context = {}
    ranks, problems = Scoreboard.results()

    # Get information (fname, lname) for each user, map user object over id
    profiles = Profile.objects.select_related('user').in_bulk(map(lambda x: x[0], ranks))
    context['scoreboard'] = map(lambda y: (profiles[y[0]].user, y[1], y[2], y[3]), ranks)
    context['problems'] = problems
    resp = render_to_response(template, context,
            context_instance=RequestContext(request))
    cache.set('scoreboard', resp)
    return resp

@is_staff
def results(request, template='scoreboard/results.html'):
    # We won't cache this since it won't be checked often and we don't want to
    # take a chance that the cache was not invalidated when reviewing results
    context = {}
    ranks, problems = Scoreboard.results()
    profiles = Profile.objects.select_related('user').in_bulk(map(lambda x: x[0], ranks))
    context['scoreboard'] = map(lambda y: (profiles[y[0]].user, y[1], y[2], y[3]), ranks)
    context['problems'] = problems

    return render_to_response(template, context,
            context_instance=RequestContext(request))
