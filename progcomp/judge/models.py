import os
from collections import deque
from contextlib import contextmanager

from django.db import models
from django.conf import settings
from django.template import loader
from django.core.files.base import ContentFile

from progcomp.submission.models import Submission

class Result(models.Model):
    submission  = models.OneToOneField(Submission)
    status      = models.CharField(max_length=32)
    created     = models.DateTimeField(auto_now_add=True)
    diff        = models.FileField(blank=True, upload_to=lambda i,f=None: \
                    os.path.join(i.submission.registrant.user_directory('diff'), str(i.submission.id)))

    @property
    @contextmanager
    def expected_output_file(self):
        with self.submission.attempt.expected_output_file as f:
            yield f

    @property
    @contextmanager
    def user_output_file(self):
        with self.submission.user_output_file as f:
            yield f

    def grade(self, save=True):
        with self.expected_output_file as expected_file:
            with self.user_output_file as user_file:
                # Read the output into an array
                expected_output = [x.strip() for x in expected_file if x.strip() != '']
                try:
                    # Make sure our output can be parsed as ASCII (i.e., they didn't upload an executable)
                    user_output = [unicode(x.strip()) for x in user_file if x.strip() != '']
                except UnicodeDecodeError:
                    self.status = 'invalid file encoding'

                else:
                    if expected_output != user_output:
                        self.create_diff(expected_output, user_output)
                        self.status = 'failed'
                    else:
                        self.status = 'success'
        if save:
            self.save()
        return self.status == 'success'

    def create_diff(self, expected_output, user_output):
        # Create diff file - We must convert to string because writing original type will give characters
        diffs, err_left = self.compute_diff(expected_output, user_output)
        content = loader.render_to_string('_diff_stub.html', {'diffs': diffs, 'err_left': err_left})
        myfile = ContentFile(str(content))

        # Remove diff file if one was created from a previous grading
        try:
            path = os.path.join(settings.MEDIA_ROOT, self.diff.field.generate_filename(self))
            os.remove(path)
        except OSError:
            pass

        self.diff.save('', myfile, save=False)

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

class SampleResult(Result):
    temp_input = None
    submission = Submission(id=0)

    @property
    @contextmanager
    def expected_output_file(self):
        with open(os.path.join(settings.MEDIA_ROOT, 'sample.out')) as f:
            yield f

    @property
    @contextmanager
    def user_output_file(self):
        with self.temp_input as f:
            yield f

    def __init__(self, temp_input, user, *args, **kwargs):
        self.temp_input = temp_input
        self.submission.registrant = user
        super(SampleResult, self).__init__(*args, **kwargs)
