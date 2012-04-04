import filecmp

from time import sleep

from django.core.management.base import BaseCommand, CommandError
from progcomp.submission.models import *
from progcomp.judge.models import *
from progcomp.file_creation_utils import create_compiled_output
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models.fields.files import FieldFile

from collections import deque

class Command(BaseCommand):
    can_import_settings = True
    help = 'Starts the grading service, that grades new submissions every thirty seconds.'

    def compute_diff(self, expected, given, context=2):
        # Note: both inputs are assumed stripped of whitespace and blank lines
        # Make sure that no excess output is given on either side
        while len(given) < len(expected):
            given.append(None)
        while len(expected) < len(given):
            expected.append(None)

        # Collect points of error
        errors = deque([n for n, line in enumerate(expected) if expected[n] != given[n]])

        # Collect lines with context
        diff = []
        for n, line in enumerate(expected):
            # Clear error that we've already copied
            if n > errors[0] + context:
                errors.popleft()
                if len(errors) == 0: break
            # Append line if part of error
            if n >= errors[0] - context and n <= errors[0] + context:
                diff.append((n, line, given[n]))

        return diff

    def handle(self, *args, **options):
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
                    # myfile = ContentFile(diff.make_file(expected_output,output,'expected','given',True,3))
                    myfile = ContentFile('\n'.join(['\t'.join([a[1]!=a[2] and "-" or " "]+map(lambda a:str(a),a)) for a in self.compute_diff(expected_output, output)]))
                    
                    calculated_result.diff.save(attempt.problem.slug+'_%d'%attempt.inputCases+'.txt',myfile)
                    calculated_result.status = 'failed'
                else:
                    calculated_result.status = 'success' 
                
                calculated_result.save()
            sleep(5)
