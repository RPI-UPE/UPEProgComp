import os.path
import mimetypes

from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.conf import settings

from progcomp.account.models import is_registered
from progcomp.utils import serve_file
from progcomp.scoreboard.models import ScoreboardAccess

@is_registered
def diff(request, diffid, tiny=False, template='judge/diff.html'):
    # Get user dir
    userdir = request.user.profile.user_directory('diff')

    # Check to make sure path exists
    path = os.path.join(settings.MEDIA_ROOT, userdir, diffid)
    if not os.path.exists(path):
        raise Http404

    # If we are using the tiny flag, we can just return the file directly
    if tiny:
        return serve_file(request, path)

    # Read file to string and embed in template
    with open(path) as fh:
        diff_content = mark_safe(fh.read())

    return render_to_response(template, {'diff_content': diff_content},
            context_instance=RequestContext(request))

@is_registered
def input(request, slug, direct=False):
    # Get user dir
    userdir = request.user.profile.user_directory('input')

    # Check to make sure path exists
    path = os.path.join(settings.MEDIA_ROOT, userdir, slug + '.in')
    if not os.path.lexists(path):
        raise Http404

    return serve_file(request, path, force_download=direct)

@is_registered
def resume(request, user_id=None, access_code=None):
    user = request.user
    if user_id and (request.user.is_staff or ScoreboardAccess.valid(access_code)):
        try:
            user = User.objects.select_related('profile').get(pk=user_id)
        except ScoreboardAccess.DoesNotExist:
            raise Http404

    if not user.profile.resume:
        raise Http404

    path = user.profile.resume.path
    resume_type = mimetypes.guess_type(path)[0] or 'application/force-download'
    return serve_file(request, path,  force_download=False, content_type=resume_type)
