import filecmp

from time import sleep

from django.core.management.base import BaseCommand, CommandError
from progcomp.submission.models import *
from progcomp.judge.models import *
from progcomp.file_creation_utils import decode_to_list, create_compiled_output
from django.conf import settings
from django.core.files.base import ContentFile

import difflib

class Command(BaseCommand):

    can_import_settings = True
    help = 'Starts the grading service, that grades new submissions every thirty seconds.'

    def handle(self, *args, **options):
        diff = difflib.HtmlDiff()
        while True:

            S = Submission.objects.filter(result=None)

            for current_submission in S:
                attempt = current_submission.attempt

                expected_output = open(create_compiled_output(attempt.problem.slug,attempt.input_cases)).readlines()
                output = open(settings.MEDIA_ROOT+'/'+current_submission.output_file.name).readLines()
                
                expected_output = [x.strip() for x in expected_output if x.strip() != ''] 
                output = [x.strip() for x in output if x.strip() != ''] 

                calculated_result = Result()
                calculated_result.submission = current_submission
			    
                if(expected_output != output):
                    #### I DON'T KNOW IF THIS WORKS
                    myfile = ContentFile(diff.make_table(expected_output,output,'expected','given',True,3))
                    
                    calculated_result.diff = FileField.save(attempt.problem.slug+'_%d'%attempt.input_cases+'.html',myfile)
                    calculated_result.status = 'failed'
                else:
                    calculated_result.status = 'success' 
                
                calculated_result.save()
            sleep(5)
