import os
from contextlib import contextmanager

from django.db import models
from django.conf import settings

class Problem(models.Model):

    slug = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=32)
    available_inputs = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def path(self):
        path = os.path.join(settings.GRADE_DIR, self.slug)
        if os.path.exists(path):
            return path
        raise Exception('Problem directory does not exist')

    @contextmanager
    def expected_output_file(self, input_id):
        with open(os.path.join(self.path, '%d.out' % input_id)) as f:
            yield f
