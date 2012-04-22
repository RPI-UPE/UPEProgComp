import sys
import random
import math
import string
"""
The imports above are really usefull
for test case generation.  You will 
probably use them.
"""


def test(nmax=10**4):
    """
    define a test case generator in this 
    file.  Test cases generators should
    return a single test case without a trailing
    newline.
    """
    return "%d"%(random.randint(1,nmax))

