import time
from django.db import models

class Report(models.Model):
    view = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    calls = models.IntegerField()
    time = models.FloatField()
    timer = None

    def start(self):
        if self.timer:
            self.end()
        self.timer = time.time()

    def end(self, increment=True):
        if self.timer:
            self.time += time.time() - self.timer
            self.timer = None
            if increment:
                self.calls += 1