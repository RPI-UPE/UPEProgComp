import filecmp

from time import sleep

from django.core.management.base import BaseCommand, CommandError
from progcomp.submission.models import *
from progcomp.judge.models import *
from progcomp.file_creation_utils import decode_to_list, create_compiled_output
from django.conf import settings

import difflib

class Command(BaseCommand):

    can_import_settings = True
    help = 'Starts the grading service, that grades new submissions every thirty seconds.'

    def handle(self, *args, **options):
        #A = difflib.Differ()
        while True:

            S = Submission.objects.filter(result=None)

            for current_submission in S:
                attempt = current_submission.attempt
                input_cases = decode_to_list(attempt.inputCases)

                expected_output = create_compiled_output(attempt.problem.slug,input_cases)
                output = open(settings.MEDIA_ROOT+'/'+current_submission.output_file.name).read()

                calculated_result = Result()
                calculated_result.submission = current_submission
			    
                output = output.strip()
                expected_output = expected_output.strip()

                #output_split = output.split('\n')
                #expected_split = expected_output.split('\n')
                
                #print "%d == %d"%(len(output), len(expected_output))

                #y = ['*'.join(x) for x in zip(output_split,expected_split)]
                
                #print '\n'.join(y)

                if(expected_output != output):
                    calculated_result.status = 'failed'
                else:
                    calculated_result.status = 'success'
                
                calculated_result.save()
            sleep(5)
