import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def index(request, template='index.html'):
    return render_to_response(template, context_instance=RequestContext(request))

def rules(request, template='rules.html'):
    return render_to_response(template, context_instance=RequestContext(request))

def contact(request, template='contact.html'):
    return render_to_response(template, context_instance=RequestContext(request))

def notyet(request, template='notyet.html'):
    return render_to_response(template,
            context_instance=RequestContext(request))
