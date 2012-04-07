import datetime
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction

from progcomp.utils import handle_upload_file
from progcomp.account.forms import RegistrationForm
from progcomp.account.forms import ProfileForm
from progcomp.account.models import Profile
from progcomp.submission.models import Submission
from progcomp.account.models import is_registered


@transaction.commit_on_success
def register(request, template='account/register.html'):
    if Profile.objects.count() > settings.MAX_REGISTRATIONS:
        messages.error(request, "There were some errors in creating your account.")
        form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. You are now logged in.")
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = RegistrationForm()
    return render_to_response(template, {'form': form},
            context_instance=RequestContext(request))

@is_registered
def index(request, template='account/index.html'):
    context = {}
    context['submissions'] = Submission.user_summary(request.user.profile)[:5]
    context['is_started'] = settings.START < datetime.datetime.now()
    return render_to_response(template, context,
            context_instance=RequestContext(request))


@is_registered
def edit_profile(request, template='account/edit.html'):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # request.user.profile.grad = form.cleaned_data['grad']
            # resume = form.cleaned_data['resume']
            # if resume is not None:
            #     udir = os.path.join(settings.MEDIA_ROOT, 'resumes/')
            #     path = handle_upload_file(resume, request.user.username, request.user.profile.first_name,
            #             request.user.profile.last_name, udir)
            #     request.user.profile.resume = path[len(settings.MEDIA_ROOT):]
            # request.user.profile.save()
            messages.success(request, "Profile saved.")
            return HttpResponseRedirect(reverse('profile'))
    else:
        # raise Exception(ProfileForm().Meta)
        form = ProfileForm(instance=request.user.profile)

    return render_to_response(template, {'form': form},
            context_instance=RequestContext(request))
