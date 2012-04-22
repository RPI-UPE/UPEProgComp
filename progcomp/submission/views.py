import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from progcomp.submission.forms import SubmissionForm
from progcomp.submission.models import Submission, Attempt
from progcomp.problems.models import Problem
from progcomp.account.models import is_registered
from progcomp.decorators import during_competition


@is_registered
def download(request, template = 'submission/download_page.html'):
    if request.method == 'GET':
        problems = Problem.objects.all()
        submissions = Submission.user_summary(request.user)

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

        context = {
            'submissions':submissions,
            'problems':problems
        }
        return render_to_response( template, context,
                context_instance=RequestContext(request))

    else:
        # This shouldn't happen.
        # Page should only get GET requests
        pass

@is_registered
@transaction.commit_on_success
def submit(request, problem_id='-1', template='submission/submission_form.html'):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        
        # Check if there is an available attempt within the time limit
        try:
            recent_attempt = Attempt.objects.filter(person=request.user.profile, problem__id=problem_id, submission=None).latest('startTime')
        except Attempt.DoesNotExist:
            recent_attempt = None

        if recent_attempt and form.is_valid():
            if recent_attempt.time_since() > settings.ATTEMPT_DURATION:
                messages.error(request, "Time limit exceeded. Please download a new input file and submit your new output.")
                return HttpResponseRedirect(reverse('submit', args=[recent_attempt.problem.id]))

            submission = form.save(commit=False)
            submission.registrant = request.user.profile
            submission.attempt = recent_attempt
            submission.save()
            messages.success(request, "Submission received. It will be graded shortly.")
            return HttpResponseRedirect(reverse('download'))
        else:
            messages.error(request, "Error submitting files. Please make sure you are uploading a source and output file and that neither are empty.")
            return HttpResponseRedirect(reverse('submit', args=[recent_attempt.problem.id]))
    else:
        context = {}

        # Check if there is an available attempt within the time limit
        try:
            recent_attempt = Attempt.objects.filter(person=request.user.profile, problem__id=problem_id, submission=None).latest('startTime')
            total_seconds = recent_attempt.time_since()
        except Attempt.DoesNotExist:
            recent_attempt = None

        if recent_attempt and total_seconds < settings.ATTEMPT_DURATION:
            current_attempt = recent_attempt
        else:
            # Create new attempt
            total_seconds = 0
            current_attempt = Attempt.create(request.user, problem_id)
            current_attempt.save()

        context['input_path'] = reverse('input_direct', args=(current_attempt.problem.slug,))
        context['input_path_view'] = reverse('input', args=(current_attempt.problem.slug,))
        context['form'] = SubmissionForm()
        context['problem_name'] = current_attempt.problem.name
        context['problem_id'] = current_attempt.problem.id
        context['max_time_display'] = "%d:%02d" % (settings.ATTEMPT_DURATION/60, settings.ATTEMPT_DURATION%60)
        context['max_time'] = settings.ATTEMPT_DURATION
        context['elapsed_time'] = total_seconds
        context['remaining_time'] = settings.ATTEMPT_DURATION - total_seconds
        context['refresh_time'] = settings.ATTEMPT_DURATION / 2

    return render_to_response(template, context, context_instance=RequestContext(request))

@is_registered
@during_competition
def refresh(request, problem_id='-1', template='submission/submission_form.html'):
    # Check if we are under half time remaining
    try:
        recent_attempt = Attempt.objects.filter(person=request.user.profile, problem__id=problem_id, submission=None).latest('startTime')
        if recent_attempt.time_since() >= settings.ATTEMPT_DURATION / 2:
            # Force-create a most-recent problem
            Attempt.create(request.user, problem_id).save()
    except:
        pass

    return HttpResponseRedirect(reverse('submit', args=[problem_id]))

def json(request, template = 'submission/download_page.html'):
    import json
    from django.template.defaultfilters import capfirst
    # The submission ids that we are looking for are sent via GET
    try:
        ids = map(lambda x: int(x), request.GET.get('submissions', '').split(','))
        graded = Submission.user_summary(request.user).filter(pk__in=ids).exclude(result=None)
        graded = dict([(sub.id, sub.result.diff and reverse('diff', args=[sub.id]) or capfirst(sub.result.status)) for sub in graded])
    except ValueError:
        # Invalid value for submissions, int() failed
        graded = {}
    response = json.dumps(graded)
    response = HttpResponse(response, mimetype='application/json')
    response['Cache-Control'] = 'no-cache'
    return response
