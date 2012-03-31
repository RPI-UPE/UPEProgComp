import hashlib
import mimetypes
import os
import shutil
from tempfile import mkstemp


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