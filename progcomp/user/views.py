import os.path

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe

from progcomp.judge.models import Result
from progcomp.account.models import is_registered
from progcomp.utils import serve_file
from progcomp.file_creation_utils import user_grade_dir_name

from settings import MEDIA_ROOT

@is_registered
def diff(request, diffid, tiny=False, template='judge/diff.html'):
    try:
        diff = Result.objects.get(id=diffid, submission__registrant=request.user.profile)
    except Result.DoesNotExist:
        diff = None

    # If we didn't find the diff record or the diff file
    # Do this in two steps because we don't know if diff.diff is available
    if not diff or not diff.diff:
        raise Exception("Invalid diff")
    path = os.path.join(MEDIA_ROOT, str(diff.diff))
    if not os.path.exists(path):
        raise Exception("Invalid diff")

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
    userdir = os.path.join(MEDIA_ROOT, 'users/', user_grade_dir_name(request.user.username))

    # Check to make sure path is clean and exists
    path = os.path.join(userdir, slug + '.in')
    if not path.startswith(userdir) or not os.path.lexists(path):
        raise Exception("Invalid problem slug")

    return serve_file(request, path, force_download=direct)
