import os

from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.views import static

from settings import USING_NGINX, MEDIA_ROOT

def serve_file(request, path, force_download=False):
    fs_path = os.path.join(MEDIA_ROOT, path)
    if not os.path.exists(fs_path):
        raise Exception("File not found: %s" % fs_path)

    filename = os.path.basename(path)
    if USING_NGINX:
        # We can form an HTTP response and let nginx handle the rest
        if force_download:
            response = HttpResponse(mimetype='application/force-download')
        else:
            response = HttpResponse(mimetype='')
        response['X-Accel-Redirect'] = smart_str(path)

        return response

    else:
        # In development, we can just use Django's static serve
        resp = static.serve(request, filename, show_indexes=False,
                document_root=os.path.dirname(fs_path))
        if not force_download:
            resp['Content-Type'] = '' # Display in browser
        return resp
