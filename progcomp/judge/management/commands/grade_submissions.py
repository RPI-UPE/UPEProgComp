import datetime
from time import sleep
from collections import defaultdict

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.conf import settings

from progcomp.stats.models import Report
from progcomp.judge.models import Result
from progcomp.submission.models import Submission

class Command(BaseCommand):
    can_import_settings = True
    help = 'Starts the grading service, that grades new submissions every thirty seconds.'

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
                calculated_result = Result(submission=current_submission)
                if calculated_result.grade():
                    cache.delete('scoreboard')
                
                print log[calculated_result.status] % calculated_result.log_string

                # Increment profiler each iteration
                stats.end()

            # Commit profiler every 5 graded if we are running profiler
            if settings.PROFILER:
                if stats.calls >= next_commit['calls'] and datetime.datetime.now() >= next_commit['time']:
                    stats.save()
                    next_commit['calls'] = stats.calls + 1
                    next_commit['time']  = datetime.datetime.now() + datetime.timedelta(seconds=COMMIT_DELTA)
            sleep(1)
