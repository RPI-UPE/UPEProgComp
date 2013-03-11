import os
import datetime
from time import sleep
from collections import deque, defaultdict

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from django.template import loader

from progcomp.stats.models import Report
from progcomp.judge.models import Result
from progcomp.submission.models import Submission

class Command(BaseCommand):
    can_import_settings = True
    help = 'Starts the grading service, that grades new submissions every thirty seconds.'

    # compute_diff() takes two arrays and returns an array with errors in matching
    # returns: - list of tuples for relevant lines in the form (line_no, expected, given)
    #          - number of errors truncated
    # Note: both inputs are assumed stripped of whitespace and blank lines
    def compute_diff(self, expected, given, context=2, errors=2):
        # Make sure that no excess output is given on either side
        while len(given) < len(expected):
            given.append(None)
        while len(expected) < len(given):
            expected.append(None)

        # Collect points of error
        errlist = [n for n, line in enumerate(expected) if expected[n] != given[n]]
        err_ct = len(errlist)
        errlist = deque(errlist[:errors])

        # Collect lines with context
        diff = []
        for n, line in enumerate(expected):
            # Clear error that we've already copied
            if n > errlist[0] + context:
                errlist.popleft()
                if len(errlist) == 0: break
            # Append line if part of error
            if n >= errlist[0] - context and n <= errlist[0] + context:
                diff.append((n+1, line, given[n]))

        return diff, err_ct - sum(1 for e in diff if e[1] != e[2])

    # Arguments:
    #   regrade [<slug>] - remove and regrade all failed results for the given
    #                      problem, or all results if no slug is provided
    def handle(self, *args, **options):
        # Parse arguments
        if len(args) > 0 and args[0] == "regrade":
            where = { 'status': 'failed' }
            if len(args) > 1:
                where['submission__attempt__problem__slug'] = args[1]
            try:
                res = Result.objects.all().filter(**where)
                print "Deleting %d results" % len(res)
                res.delete()
            except:
                pass

        # Setup colored logging
        log = defaultdict(lambda: '%s', {'success': '\033[32m%s\033[0m'})

        # Setup stat reporting
        stats = None
        COMMIT_DELTA = 5
        stats = Report(view='grade_submissions', method='CONSOLE')
        next_commit = {'calls': stats.calls + 1,
                       'time': datetime.datetime.now() + datetime.timedelta(seconds=COMMIT_DELTA) }

        # Begin processing
        while True:

            stats.start()
            S = Submission.objects \
                    .select_related('attempt', 'attempt__problem', 'result') \
                    .filter(result=None)
            stats.end(increment=False)

            for current_submission in S:
                stats.start()
                attempt = current_submission.attempt
                
                # Create the result
                calculated_result = Result()
                calculated_result.submission = current_submission

                with open(attempt.output_path) as expected_file:
                    with open(os.path.join(settings.MEDIA_ROOT, current_submission.output_file.name)) as output_file:
                        # Read the output into an array
                        expected_output = [x.strip() for x in expected_file if x.strip() != '']
                        try:
                            # Make sure our output can be parsed as ASCII (i.e., they didn't upload an executable)
                            output = [unicode(x.strip()) for x in output_file if x.strip() != '']
                        except UnicodeDecodeError:
                            status = 'invalid file encoding'

                        else:
                            if expected_output != output:
                                # Create diff file - We must convert to string because writing original type will give characters
                                diffs, err_left = self.compute_diff(expected_output, output)
                                content = loader.render_to_string('_diff_stub.html', {'diffs': diffs, 'err_left': err_left})
                                myfile = ContentFile(str(content))

                                # Remove diff file if one was created
                                path = calculated_result.diff.field.generate_filename(calculated_result)
                                if os.path.exists(path):
                                    os.remove(path)

                                calculated_result.diff.save('', myfile)
                                status = 'failed'
                            else:
                                status = 'success'
                                cache.delete('scoreboard')
                
                calculated_result.status = status
                calculated_result.save()
                print log[status] % ("[%s] Graded %s by %s: %s" % (datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S"),
                        attempt.problem.slug, attempt.person, status))

                # Increment profiler each iteration
                stats.end()

            # Commit profiler every 5 graded if we are running profiler
            if settings.PROFILER:
                if stats.calls >= next_commit['calls'] and datetime.datetime.now() >= next_commit['time']:
                    stats.save()
                    next_commit['calls'] = stats.calls + 1
                    next_commit['time']  = datetime.datetime.now() + datetime.timedelta(seconds=COMMIT_DELTA)
            sleep(1)
