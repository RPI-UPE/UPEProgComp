def default_gen(problem_name='test'):
    """default_gen generates the default
    test cases by reading in the
    file defaults/${problem_name}.txt
    see defaults/README for information on
    what the file should contain
    """
    f = open('defaults/%s.txt'%problem_name)
    all_lines = f.readlines()
    arr = all_lines[1:]
    num = int(all_lines[0])
    f.close()
    return (num,''.join(arr))
