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


def http_basic_auth(realm='Django App'):
    def _inner(func):
        def decorator(request, *args, **kwargs):
            response = HttpResponse('401 Unauthorized', 'text/plain', 401)
            response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
            if 'HTTP_AUTHORIZATION' in request.META:
                method, enc = request.META['HTTP_AUTHORIZATION'].split(' ')
                if method != 'Basic':
                    return response
                user, passwd = base64.b64decode(enc).split(':', 1)
                user = authenticate(username=user, password=passwd)
                if user is not None:
                    request.user=user
                return func(request, *args, **kwargs)
            else:
                return response
        return decorator
    return _inner
