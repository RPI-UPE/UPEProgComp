import binascii
import random
import os.path
import hashlib
import settings

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
        grade_dir_name = user_grade_dir_name(username)
        target_symlink = USERS_ROOT+grade_dir_name+'/'+problem_name+'.in'
        
        link_name = GRADE_DIR+problem_name+'/%d'%selected_number+'.in' 
        
        logging.info('%s --> %s'%(link_name, target_symlink))
        
        if (os.path.lexists(target_symlink)):
            os.unlink(target_symlink)
        
        os.link(link_name, target_symlink)
        
        problem_html = USERS_URL+grade_dir_name+'/'+problem_name+'.in'
        return (selected_number,problem_html)
    else:
        raise Exception('Invalid Problem Name')

def create_compiled_output(problem_name, selected):
    if os.path.exists(GRADE_DIR+problem_name):
        return GRADE_DIR+problem_name+'/%d'%selected+'.out'
    else:
        raise Exception('Invalid Problem Name')


def user_grade_dir_name(username):
    return hashlib.md5(username).hexdigest()[0:5] + username

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
