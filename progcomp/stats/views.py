from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from progcomp.decorators import if_setting
from progcomp.stats.models import Report

@if_setting('PROFILER')
def index(request):
    stats = [r for r in sorted(Report.objects.all(), key=lambda x: -x.time)]

    if len(stats) > 0:
        total_calls, total_time = map(lambda t: sum(t), zip(*[(r.calls, r.time) for r in stats]))

        for r in stats:
            r.avg = r.time / r.calls
            r.perc = r.time / total_time * 100.0

    context = { 'stats': stats, }
    return render_to_response('stats/index.html', context, context_instance=RequestContext(request))


@if_setting('PROFILER')
def reset(request):
    Report.objects.all().delete()
    messages.info(request, "All data cleared")
    return HttpResponseRedirect(reverse('stats'))
