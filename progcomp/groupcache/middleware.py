from django.middleware.cache import CacheMiddleware

from groupcache.core import logger, \
    get_view_name, get_local_key, get_local_prefix, bump_local_prefix

from groupcache.utils import _bumping_cache

#-------------------------------------------------------------------------------
class CacheWithLocalVersionMiddleware(CacheMiddleware):
    def __init__(self, group = None, view_func = None,
                 vary_on_view = True, *args, **kwargs):
        super(CacheWithLocalVersionMiddleware, self).__init__(*args, **kwargs)
        self.base_key_prefix = self.key_prefix
        self.group =  group
        view_name = get_view_name(view_func)
        self.view_name = view_name if vary_on_view is True else None
        _bumping_cache[view_name] = (group, vary_on_view)
        #logger.debug('Bumping: %s', repr(_bumping_cache))

    def _update_key_prefix(self, view_keywords):
        self.key_prefix = get_local_prefix(
            get_local_key(
                self.group, view_keywords,
                self.view_name, self.base_key_prefix),
            self.base_key_prefix)
        #logger.debug('Key prefix: %s' % repr(self.key_prefix))

    def process_response(self, request, response):
        # See process_view()
        return response

    def process_request(self, request):
        # See process_view()
        pass

    def process_view(self, request, view_func, view_args, view_keywords):
        # This middleware is a derivated from CacheMiddleware:
        #
        # we move cache action from process_request() to and process_response(),
        # because we might need to compute the group key from
        # the view keywords.
        if len(view_args) != 0:
            raise TypeError(
                'locally versionned view should exclusively use keywords')
        self._update_key_prefix(view_keywords)
        response = super(CacheWithLocalVersionMiddleware,
                         self).process_request(request)
        if response is not None:
            logger.debug('page found in cache')
            return response
        else:
            # The per-view decorator we will get out of this middleware (using
            # django.utils.decorators.decorator_from_middleware) behaves
            # slightly differently than a fully-fledged middleware. The official
            # doc states (Django 1.2, 1.3):
            #
            # Unlike the process_request() and process_view() methods, the
            # process_response() method is always called, even if the
            # process_request() and process_view() methods of the same
            # middleware class were skipped because an earlier middleware method
            # returned an HttpResponse (this means that your process_response()
            # method cannot rely on setup done in process_request(), for
            # example)
            #
            # This does not hold for the derivated decorators: in this case,
            # process_response() is only called if process_view() returns
            # nothing, and it's safe to share states between the two methods (go
            # read django.utils.decorators.make_middleware_decorator).
            response = view_func(request, *view_args, **view_keywords)
            #logger.debug('Caching! %s' % repr(self.key_prefix)
            return super(CacheWithLocalVersionMiddleware,
                         self).process_response(request, response)
