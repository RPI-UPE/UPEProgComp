import os

def default_gen(problem_name='test'):
    """default_gen generates the default
    test cases by reading in the
    file defaults/${problem_name}.txt
    see defaults/README for information on
    what the file should contain
    """
    
    #this lets us open the default directory
    #relative to this script no matter where we
    #are called from.
    scriptpath = os.path.dirname(__file__)
    
    f = open('%s/defaults/%s.txt'%(scriptpath,problem_name))
    all_lines = f.readlines()
    arr = all_lines[1:]
    num = int(all_lines[0])
    f.close()
    return (num,''.join(arr))
