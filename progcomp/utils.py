import os

from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.views import static
from django.conf import settings

def serve_file(request, fs_path, force_download=False, content_type='text/plain'):
    # The filesystem path is specified in the argument, whereas nginx expects a
    # URI in the header
    path = os.path.join(settings.MEDIA_URL, os.path.relpath(fs_path, settings.MEDIA_ROOT))

    if not os.path.exists(fs_path):
        raise Exception("File not found: %s" % fs_path)

    filename = os.path.basename(path)
    if settings.USING_NGINX:
        # We can form an HTTP response and let nginx handle the rest
        response = HttpResponse()
        response['X-Accel-Redirect'] = smart_str(path)
    else:
        # In development, we can just use Django's static serve
        response = static.serve(request, filename, show_indexes=False,
                document_root=os.path.dirname(fs_path))

    if force_download:
        response['Content-Type'] = 'application/force-download'
    else:
        # We can't set this to text/plain because we serve pdfs through here too
        response['Content-Type'] = content_type

    response['Cache-Control'] = 'no-cache'
    return response

def user_upload(subdir, dest_name=None):
    def handle_upload(instance, filename=None):
        # File will be stored in user_directory
        path = instance.user.profile.user_directory(subdir)
        # The name of the file will be the first filename if provided
        if isinstance(dest_name, type(lambda:None)):
            filename = dest_name(instance)
        elif dest_name != None:
            filename = dest_name
        return os.path.join(path, filename)
    return handle_upload
