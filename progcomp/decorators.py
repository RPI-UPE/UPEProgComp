import datetime
import base64
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse

from progcomp.views import notyet

def during_competition(func):
    def decorator(*args, **kwargs):
        start = settings.START
        end   = settings.END
        now   = datetime.datetime.now()
        if start <= now and now < end:
            return func(*args, **kwargs)
        else:
            return notyet(args[0])
    return decorator

