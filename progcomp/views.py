import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def index(request, template='frontpage/index.html'):
    return render_to_response(template, context_instance=RequestContext(request))


def notyet(request, template='frontpage/notyet.html'):
    context = {}
    context['start'] = start = settings.START
    context['end']   = end   = settings.END
    context['now']   = now   = datetime.datetime.now()
    if start <= now and now < end:
        return HttpResponseRedirect(reverse('profile'))
    return render_to_response(template, context,
            context_instance=RequestContext(request))
