import time

from django.core.urlresolvers import resolve
from django.conf import settings

from progcomp.stats.models import Report

class ProfilingMiddleware:
    report = None
    state = 'new'

    def check_filters(self, view):
        for f in settings.PROFILER_FILTERS:
            if f.match(view):
                return True
        return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        view = resolve(request.META['PATH_INFO']).url_name
        method = request.method

        if self.state != 'new' or not settings.PROFILER or self.check_filters(view):
            return

        try:
            self.report = Report.objects.get(view=view, method=method)
        except Report.DoesNotExist:
            self.report = Report(view=view, method=method, calls=0, time=0)

        self.report.calls += 1
        self.startTime = time.time()
        self.state = 'view'

    def process_response(self, request, response):
        if self.state == 'view' and self.report:
            self.report.time += time.time() - self.startTime
            self.report.save()
            self.state = 'new'
        return response

    def process_exception(self, request, exception):
        self.state = 'invalid'
        return None
