import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import transaction
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from progcomp.submission.forms import SubmissionForm
from progcomp.submission.models import Submission
from progcomp.submission.models import Attempt
from progcomp.utils import handle_upload_file

from progcomp.account.models import is_registered
from progcomp.decorators import during_competition
from progcomp.file_creation_utils import *

from progcomp.problems.models import *

import datetime
from django.conf import settings

@is_registered
@during_competition
def download(request, template = 'submission/download_page.html'):
    if request.method == 'GET':
        problems = Problem.objects.values('id', 'name')
        return render_to_response( template, {'problems' : problems}, context_instance=RequestContext(request))

    else:
        # This shouldn't happen.
        # Page should only get GET requests
        pass

@is_registered
@during_competition
@transaction.commit_on_success
def submit(request, template='submission/submission_form.html'):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        
        #temp = form['problem'].value()
        #_problem = Problem.objects.get(id=temp)
        someAttempt = Attempt.objects.filter(person = request.user.profile).order_by('-startTime')

        timediff = datetime.datetime.now() - someAttempt[0].startTime

        if form.is_valid():
            
            total_seconds = (timediff.microseconds + (timediff.seconds + timediff.days * 24 * 3600) * 10**6) / 10**6
            if total_seconds > settings.ATTEMPT_DURATION:
                return HttpResponseRedirect(reverse('too_late'))

            submission = form.save(commit=False)
            submission.registrant = request.user.profile
            submission.attempt = someAttempt[0]
            submission.save()
            return HttpResponseRedirect(reverse('submit-success'))
        else:
            return HttpResponseRedirect(reverse('submit-failure'))
    else:
        problem_id = request.GET.get('problem_id', -1)

        newAttempt = Attempt()
        newAttempt.person = request.user.profile
        newAttempt.problem = Problem.objects.get(pk = problem_id)
        result = create_test_input(newAttempt.problem.slug,newAttempt.problem.number_in_problem,newAttempt.problem.number_test)
        newAttempt.inputCases = result[0]
        newAttempt.startTime = datetime.datetime.now()
        newAttempt.save()

        form = SubmissionForm()

    return render_to_response(template, {'form': form, 'test_data' : result[1]},
            context_instance=RequestContext(request))

@is_registered
@during_competition
def success(request, template='submission/success.html'):
    return render_to_response(template,
            context_instance=RequestContext(request))

def failure(request, template='submission/failure.html'):
    return render_to_response(template,
            context_instance=RequestContext(request))

@is_registered
@during_competition
def too_late(request, template = 'submission/too_late.html'):
    return render_to_response(template,
            context_instance=RequestContext(request))
