import datetime

from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from progcomp.account.models import Profile
from progcomp.scoreboard.models import Scoreboard, ScoreboardAccess
from progcomp.account.models import is_staff

def render_cached(cached, request):
    return render_to_response('scoreboard/scoreboard.html', {'cache':cached},
            context_instance=RequestContext(request))

def scoreboard(request, access_code=None, template='scoreboard/_cacheboard.html'):
    if not request.user.is_staff and not ScoreboardAccess.valid(access_code, increment=True):
        # Check the cache for a response object and return that if set. We're not
        # using Django's view/template cacher because we cannot invalidate them.
        sb_cache = cache.get('scoreboard')
        if sb_cache:
            return render_cached(sb_cache, request)
        context = {}
    else:
        # If the user is a staff, we show the extended results page
        # We won't cache this since it won't be checked often and we don't want to
        # take a chance that the cache was not invalidated when reviewing results
        context = {'results': True, 'template_fullwidth': True}

    # Get information (fname, lname) for each user, map user object over id
    ranks, problems = Scoreboard.results()
    profiles = Profile.objects.select_related('user').in_bulk(map(lambda x: x[0], ranks))
    context['scoreboard'] = map(lambda y: (profiles[y[0]].user, y[1], y[2], y[3]), ranks)
    context['problems'] = problems
    # Default this to "" so that the resume links work
    context['access_code'] = access_code or ""

    resp = render_to_string(template, context,
            context_instance=RequestContext(request))
    if not request.user.is_staff:
        cache.set('scoreboard', resp)
    return render_cached(resp, request)
