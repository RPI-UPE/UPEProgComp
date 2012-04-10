from django.conf import settings

def profiler(context):
    return {'PROFILER': settings.PROFILER}
