import os

from problem_creation.defaults import default_gen as default
import problem_creation.generator as generator
OUTPUT_DIR = '.'

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



def create_all_files(problem_name,number_of_files=100,number_input_cases=100):
    """
    Creates the default function from the problem name,
    and retrieves the generator function from the generator.py
    file.  It then calls the create_file function number_of_files
    times to create a file with number_input_cases test cases.
    """

    default_function = lambda: default(problem_name)
    generate_function = getattr(generator,problem_name)
    
    output_path = '%s/%s'%(OUTPUT_DIR,problem_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for i in range(number_of_files):
        create_file('%s/%d.in'%(output_path,i),
                default_function,generate_function,number_input_cases)

def create_output(command, input_file, output_file, output_type = 1):
    if output_type == 0: 
        # if the script takes input and output files
        fullcommand = "time "+command+" "+input_file+" "+output_file;
        os.system(fullcommand) 
    if output_type == 1: 
        # if the script takes an input and outputs to std
        fullcommand = "time "+command+" "+input_file+" >"+output_file;
        os.system(fullcommand)

def create_all_output(command, input_dir, number_of_files=100):
    
    for i in range(number_of_files):
        create_output(command,"%s/%d.in"%(input_dir,i),"%s/%d.out"%(input_dir,i))

if __name__ == '__main__':
    create_all_files('test',2,100)
    create_all_output('python solutions/test.py', 'test',2)
