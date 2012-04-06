import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
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
        problems = Problem.objects.all()
        submissions = Submission.user_summary(request.user.profile)

        correct = set()
        for sub in submissions:
            # Because we don't know if there is a result yet, and it is not a
            # member of the Submission model, we need to use a try-except block
            try:
                if sub.result.status == 'success':
                    correct.add(sub.attempt.problem.slug)
            except:
                pass

        problems = [(p.id, p.name, p.slug in correct) for p in problems]

        context = {}
        context['submissions'] = submissions
        context['problems'] = problems
        return render_to_response( template, context,
                context_instance=RequestContext(request))

    else:
        # This shouldn't happen.
        # Page should only get GET requests
        pass

@is_registered
@during_competition
@transaction.commit_on_success
def submit(request, problem_id='-1', template='submission/submission_form.html'):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        
        #temp = form['problem'].value()
        #_problem = Problem.objects.get(id=temp)
        someAttempt = Attempt.objects.filter(person = request.user.profile).order_by('-startTime')

        timediff = datetime.datetime.now() - someAttempt[0].startTime

        if form.is_valid():
            
            total_seconds = (timediff.microseconds + (timediff.seconds + timediff.days * 24 * 3600) * 10**6) / 10**6
            if total_seconds > settings.ATTEMPT_DURATION:
                messages.error(request, "Time limit exceeded. Please download a new input file and submit your new output.")
                return HttpResponseRedirect(reverse('submit', args=[someAttempt[0].problem.id]))

            submission = form.save(commit=False)
            submission.registrant = request.user.profile
            submission.attempt = someAttempt[0]
            submission.save()
            messages.success(request, "Submission received. It will be graded shortly.")
            return HttpResponseRedirect(reverse('download'))
        else:
            messages.error(request, "Error submitting files. Please make sure you are uploading a source and output file and that neither are empty.")
            return HttpResponseRedirect(reverse('submit', args=[someAttempt[0].problem.id]))
    else:
        context = {}

        newAttempt = Attempt()
        newAttempt.person = request.user.profile
        newAttempt.problem = Problem.objects.get(pk = problem_id)
        if not newAttempt.problem:
            raise Exception("Invalid problem id")
        # create_test_input() returns tuple (problem_number, url)
        result = create_test_input(newAttempt.problem.slug, request.user.username, newAttempt.problem.number_in_problem)
        newAttempt.inputCases = result[0]
        newAttempt.startTime = datetime.datetime.now()
        newAttempt.save()

        context['input_path'] = result[1]
        context['form'] = SubmissionForm()
        context['problem_name'] = newAttempt.problem.name
        context['max_time'] = settings.ATTEMPT_DURATION
        context['max_time_display'] = "%d:%02d" % (settings.ATTEMPT_DURATION/60, settings.ATTEMPT_DURATION%60)

    return render_to_response(template, context, context_instance=RequestContext(request))
