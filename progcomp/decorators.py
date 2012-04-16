import datetime

from django.http import Http404
from django.conf import settings

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

# Requires a key in settings to evaluate true or will 404
class if_setting(object):
    def __init__(self, key):
        self.key = key

    def __call__(self, func):
        def decorator(*args, **kwargs):
            is_set = False
            try:
                if settings.__getattr__(self.key):
                    # We can't do the actual execution because we're in a try-block
                    is_set = True
            except:
                pass

            if is_set:
                return func(*args, **kwargs)
            raise Http404

        return decorator
