import binascii
import random
import os.path
import hashlib
import settings

from settings import GRADE_DIR


key = int('a',16);


def encode(message,k=key):
    output = '%x'%(int(binascii.hexlify(message),16)^k)
    return output

def decode(message,k=key):
    print message
    return binascii.unhexlify('%x'%(int(message,16)^k))


def encode_list(message,k=key):
    return encode(" ".join([str(m) for m in message]),k)

def decode_to_list(message,k=key):
    string = decode(message,k)
    return [int(x) for x in string.split(' ')]

def chose(n,k):
    """chose k numbers from [0,n) that's 0 to n-1 inclusive"""
    x = [v+10 for v in range(n-10)]
    random.shuffle(x)
    y = range(10)+x[0:k]
    random.shuffle(y)
    return y

def create_test_input(problem_name='test',number_in_problem=100,number_test = 20):
    local_dir = GRADE_DIR    
    if(os.path.exists(GRADE_DIR+problem_name)):
        problem_set = chose(number_in_problem,number_test);
        final_problem = '%d\n'%(len(problem_set))
        for problem in problem_set:
            with open(GRADE_DIR+problem_name+'/%d_in.txt'%(problem)) as f:
                final_problem+=f.read()+'\n'
        return (encode_list(problem_set),final_problem)
    else:
        raise Error('Invalid Problem Name')       

def create_compiled_output(problem_name, problem_set):
    final_output = ''
    if os.path.exists(GRADE_DIR+problem_name):
        for problem in problem_set:
            with open(GRADE_DIR+problem_name+'/%d_out.txt'%(problem)) as f:
                final_output += f.read()+'\n'
        return final_output
    else:
        raise Error('Invalid Problem Name')


def user_grade_dir_name(username):
    return hashlib.md5(username).hex_digest()[0:5] + username

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
