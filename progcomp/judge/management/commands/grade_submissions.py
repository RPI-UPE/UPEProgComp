import filecmp

from time import sleep

from django.core.management.base import BaseCommand, CommandError
from progcomp.submission.models import *
from progcomp.judge.models import *
from progcomp.file_creation_utils import create_compiled_output
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models.fields.files import FieldFile

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
                
                with open(create_compiled_output(attempt.problem.slug,attempt.inputCases)) as tmpfile:
                    expected_output = tmpfile.readlines()

                with open(settings.MEDIA_ROOT+'/'+current_submission.output_file.name) as tmpfile:
                    output = tmpfile.readlines()
                
                expected_output = [x.strip() for x in expected_output if x.strip() != ''] 
                output = [x.strip() for x in output if x.strip() != ''] 

                calculated_result = Result()
                calculated_result.submission = current_submission
			    
                if(expected_output != output):
                    myfile = ContentFile(diff.make_file(expected_output,output,'expected','given',True,3))
                    
                    calculated_result.diff.save(attempt.problem.slug+'_%d'%attempt.inputCases+'.html',myfile)
                    calculated_result.status = 'failed'
                else:
                    calculated_result.status = 'success' 
                
                calculated_result.save()
            sleep(5)
