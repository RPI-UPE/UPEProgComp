import os

from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.views import static

from settings import USING_NGINX, MEDIA_ROOT, MEDIA_URL

def serve_file(request, path, force_download=False, content_type='text/plain'):
    # The filesystem path is in MEDIA_ROOT
    fs_path = os.path.join(MEDIA_ROOT, path)
    # Whereas nginx expects a URI in the header
    path = os.path.join(MEDIA_URL, path)

    if not os.path.exists(fs_path):
        raise Exception("File not found: %s" % fs_path)

    filename = os.path.basename(path)
    if USING_NGINX:
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
