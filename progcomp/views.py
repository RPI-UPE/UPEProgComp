import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import static

def index(request, template='frontpage/index.html'):
    return render_to_response(template, context_instance=RequestContext(request))


def notyet(request, template='frontpage/notyet.html'):
    context = {
        'start': settings.START,
        'end'  : settings.END,
        'now'  : datetime.datetime.now(),
    }
    return render_to_response(template, context,
            context_instance=RequestContext(request))
