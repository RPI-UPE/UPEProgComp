import binascii
import random
import os.path

import logging

from django.conf import settings

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

def create_compiled_output(problem_name, selected):
    if os.path.exists(settings.GRADE_DIR+problem_name):
        return settings.GRADE_DIR+problem_name+'/%d'%selected+'.out'
    else:
        raise Exception('Invalid Problem Name')

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
