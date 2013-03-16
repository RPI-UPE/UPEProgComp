import os
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from progcomp.decorators import past_competition_start
from progcomp.utils import serve_file

def index(request, template='index.html'):
    return render_to_response(template, context_instance=RequestContext(request))

def rules(request, template='rules.html'):
    return render_to_response(template, context_instance=RequestContext(request))

@past_competition_start
def problemset(request):
    path = os.path.join(settings.MEDIA_ROOT, 'problem_set.pdf')
    return serve_file(request, path, force_download=False, content_type='application/pdf')

def problemsets(request, semester):
    path = os.path.join(settings.MEDIA_ROOT, 'problem_sets', semester + '.pdf')
    return serve_file(request, path, force_download=False, content_type='application/pdf')
