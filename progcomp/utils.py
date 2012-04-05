import hashlib
import mimetypes
import os
import shutil
from tempfile import mkstemp

import os.path
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
        else:
            response = HttpResponse()
        resposne['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
        response['X-Sendfile'] = smart_str(path)
        response['Content-Length'] = os.path.getsize(path)
        return response

    else:
        # In development, we can just use Django's static serve
        return static.serve(request, filename, show_indexes=False,
                document_root=os.path.dirname(path))

def handle_upload_file(f, username, first_name, last_name, to_directory):
    '''Returns filepath of new file.'''
    fd, path = mkstemp()
    file = os.fdopen(fd, 'w')
    sha1 = hashlib.new('sha1')
    for chunk in f:
        file.write(chunk)
        sha1.update(chunk)
    file.flush()
    file.close()
    
    extension = mimetypes.guess_extension(f.content_type)
    possible_new_name = username+'_'+first_name + last_name
    new_name = possible_new_name+extension

    counter = 1

    new_path = os.path.join(to_directory, new_name)

    shutil.move(path, new_path)
    return new_path
