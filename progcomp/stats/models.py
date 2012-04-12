import time
from django.db import models
from django.db.models import F

class Report(models.Model):
    view = models.CharField(max_length=50, db_index=True)
    method = models.CharField(max_length=10, db_index=True)
    calls = models.IntegerField(default=0)
    time = models.FloatField(default=0)
    timer = None

    class Meta:
        unique_together = (('view', 'method'),)

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

    def save(self, *args, **kwargs):
        # Update old values instead of saving
        changed = Report.objects \
                      .filter(view=self.view, method=self.method) \
                      .update(calls=F('calls')+self.calls, time=F('time')+self.time)
        if changed == 0:
            # If we do fail here, we need to just make a new one
            try:
                return super(Report, self).save()
            except:
                # If this fails, it's a one-time race condition because another
                # process inserted first. We'll just discard our data since it
                # is of minimal impact.
                pass
