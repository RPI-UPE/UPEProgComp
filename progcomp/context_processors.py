import datetime

from django.conf import settings

def profiler(context):
    return {
        'PROFILER': settings.PROFILER,
        'DEBUG': settings.DEBUG,
        'START': settings.START,
        'END': settings.END,
        'NOW': datetime.datetime.now(),
    }
