import os

from django.http import HttpResponse
from django.views import static

from settings import USING_NGINX

def serve_file(request, path, force_download=False):
    if not os.path.exists(path):
        raise Exception("File not found")

    filename = os.path.basename(path)
    if USING_NGINX:
        # We can form an HTTP response and let nginx handle the rest
        if force_download:
            response = HttpResponse(mimetype='application/force-download')
            resposne['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
            response['X-Sendfile'] = smart_str(path)
            response['Content-Length'] = os.path.getsize(path)
        else:
            response = HttpResponse(mimetype='text/html')

        return response

    else:
        # In development, we can just use Django's static serve
        resp = static.serve(request, os.path.basename(path), show_indexes=False,
                document_root=os.path.dirname(path))
        if not force_download:
            resp['Content-Type'] = '' # Display in browser
        return resp
