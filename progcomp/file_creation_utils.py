import binascii
import random
import os.path

from settings import GRADE_DIR
from settings import MEDIA_ROOT
from settings import USERS_ROOT
from settings import USERS_URL

import logging

logger = logging.getLogger(__name__)

key = int('a',16);

def encode(message,k=key):
    output = '%x'%(int(binascii.hexlify(message),16)^k)
    return output

def decode(message,k=key):
    print message
    return binascii.unhexlify('%x'%(int(message,16)^k))

def chose(k):
    return random.randint(0,k-1)

def create_test_input(problem_name='test',username='test',number_in_problem=100):
    if(os.path.exists(GRADE_DIR+problem_name)):
        selected_number = chose(number_in_problem)
        target_symlink = os.path.join(MEDIA_ROOT, user_directory(username, 'input'), problem_name+'.in')
        
        link_name = os.path.join(GRADE_DIR, problem_name, str(selected_number)+'.in')
        
        logging.info('%s --> %s'%(link_name, target_symlink))
        
        if (os.path.lexists(target_symlink)):
            os.unlink(target_symlink)
        
        os.link(link_name, target_symlink)
        
        return selected_number
    else:
        raise Exception('Invalid Problem Name')

def create_compiled_output(problem_name, selected):
    if os.path.exists(GRADE_DIR+problem_name):
        return GRADE_DIR+problem_name+'/%d'%selected+'.out'
    else:
        raise Exception('Invalid Problem Name')

def user_directory(username, subdir=''):
    if username == '':
        raise Exception('Invalid user directory')
    path = os.path.join('users', username, subdir)

    # Make sure directory is accessible
    if not os.path.exists(path):
        os.makedirs(path)

    return path

if __name__ == '__main__':
    print(decode(encode('hello world')))
    print(decode(encode('what is your name')))
    print(decode(encode('what is your quest')))
    print(decode(encode('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')))
    
    cc = chose(50,10)
    print cc
    enc = decode_to_list(encode_list(cc))
    print enc
    
    (l,v) = create_test_input('test',30);
    print v
