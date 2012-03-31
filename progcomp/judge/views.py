import datetime
import hashlib
try:
    import json
except:
    import simplejson as json
import os
from django.db import transaction
from django.conf import settings
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from progcomp.submission.models import Submission
from progcomp.judge.models import Grading
from progcomp.judge.models import Result
from progcomp.judge.forms import ResultForm
from progcomp.decorators import http_basic_auth


@http_basic_auth(realm='progcomp')
@permission_required('judge.add_grading')
@permission_required('judge.add_result')
@transaction.commit_on_success
def judge(request):
    if request.method == 'POST':
        return judge_post(request)
    elif request.method == 'GET':
        return judge_get(request)
    return HttpResponseNotAllowed(['GET', 'POST'])


def judge_get(request):
    sha1 = hashlib.new('sha1')
    rand = os.urandom(4)
    sha1.update(rand)
    nonce = sha1.hexdigest()

    S = Submission.objects.filter(grading=None, result=None)
    for s in S:
        data = {}
        data['nonce']    = nonce
        data['problem']  = s.problem.slug
        data['code']     = s.sourcecode.read()
        data['result']   = s.output_file.read()
        grading = Grading(nonce=nonce, submission=s, grader=request.user)
        try:
            grading.save()
            break
        except:
            pass
    else:
        data = None

    content  = json.dumps(data)
    mimetype = 'application/json'
    response = HttpResponse(content, mimetype, 200)
    response['Content-Disposition'] = 'attachment; filename=judge.json'
    return response


def judge_post(request):
    try:
        form = ResultForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            r = Result()
            r.submission  = clean['grading'].submission
            r.grader      = clean['grading'].grader
            r.status      = clean['status']
            r.compilecode = clean['compilecode']
            r.runcode     = clean['runcode']
            r.runtime     = clean['runtime']
            r.generror    = request.POST.get('error', '')
            r.compiletext = request.POST.get('compiletext', '')
            r.runtext     = request.POST.get('runtext', '')
            r.received    = datetime.datetime.now()
            r.save()
            clean['grading'].delete()
            return HttpResponse('success', 'text/plain', 200)
        else:
            return HttpResponse('fail', 'text/plain', 200)
    except Exception, e:
        return HttpResponse('error', 'text/plain', 500)
