
def create_file(output_file,default_function,
        generate_function,number_input_cases=100):
    """
    Pass in the output file you want to write as well
    as the default and generation functions.  It will create
    a test case file with number_input_cases test cases.
    """
    with open(output_file,'w') as file:
        (num,output) = default_function()
        file.write('%d\n'%number_input_cases)
        file.write(output)
        for i in range(number_input_cases-num):
            file.write('%s\n'%generate_function())


from defaults import default_gen as default
import generator
OUTPUT_DIR = ''

def create_all_files(problem_name,number_of_files=100,number_input_cases=100)
    """
    Creates the default function from the problem name,
    and retrieves the generator function from the generator.py
    file.  It then calls the create_file function number_of_files
    times to create a file with number_input_cases test cases.
    """

    default_function = lambda: default(problem_name)
    generate_function = getattr(generator,problem_name)

    for i in range(number_of_files):
        create_file('%s/%s/%d.in'%(OUTPUT_DIR,problem_name,i),
                default_function,generate_function,number_input_cases)
