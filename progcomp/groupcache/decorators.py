from django.db.models.signals import post_save, post_delete
from django.utils.decorators import decorator_from_middleware_with_args

from groupcache.middleware import CacheWithLocalVersionMiddleware
from groupcache.core import get_view_name, \
     get_local_key_mapping, get_local_key_from_mapping, bump_local_prefix

import inspect, functools, logging

#-------------------------------------------------------------------------------
def to_fields(*local_keywords):
    '''
    Decorator to simplify introspection of to_fields callables, used by
    cache_page_for_model below:

    @to_fields("square", "inverse")
    def compute_fields(value = None):
        value = int(value)
        return {"square": value*value, "inverse": -value}

    >>> print compute_fields.local_keywords
    ("square", "inverse")
    '''
    def to_fields_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.local_keywords = local_keywords
        return wrapper
    return to_fields_decorator

#-------------------------------------------------------------------------------
def cache_versionned_page(group = None, cache_timeout = None,
                          vary_on_view = True):
    '''
    This is the most generic decorator in groupcache. Use it to
    implement whatever versionning policy you wish to have.
    '''
    def cache_versionned_page_decorator(view_func):
        return decorator_from_middleware_with_args(
            CacheWithLocalVersionMiddleware)(
            cache_timeout = cache_timeout,
            group = group,
            view_func = view_func,
            vary_on_view = True)(view_func)
    return cache_versionned_page_decorator

def cache_tagged_page(tag, cache_timeout = None):
    '''
    Decorator for extremely basic caching based on string labeling.

    from groupcache.decorators import cache_tagged_page

    @cache_tagged_page('some tag')
    def my_view(request, ...):
       ...

    Then, you can do from anywhere:

    from groupcache.utils import uncache_tag
    uncache_tag('some tag')

    An every cached page marked with the tag will get invalidated.
    '''
    assert(isinstance(tag, basestring))
    def cache_tagged_page_decorator(view_func):
        return decorator_from_middleware_with_args(
            CacheWithLocalVersionMiddleware)(
            cache_timeout = cache_timeout,
            group = tag,
            view_func = view_func,
            vary_on_view = False)(view_func)
    return cache_tagged_page_decorator

#-------------------------------------------------------------------------------
def cache_page_against_model(model, cache_timeout = None, to_fields = None):
    '''
    If you got some one-to-one relationship between a view and a model,
    you can apply this decorator to handle automatic caching invalidation
    when the entity used in a given call to the view changes.

    In the most common scenario, it\'s used like this:

    from django.http.shortcuts import get_object_or_404
    from groupcache.decorators import cache_page_for_model

    @cache_page_for_model(MyModel):
    def my_view(request, pk):
        obj = get_object_or_404(MyModel, pk=pk)
        ...

    This functionnality is the reason django-groupcache was written in
    the first place.
    '''
    def cache_page_against_model_decorator(func):
        # Retrieve django-style view name from view func
        view_name = get_view_name(func)

        # Map the view keywords to model fields using the to_fields group
        if callable(to_fields):
            raise ValueError(
                'to_fields is a specialized group that cannot be a callable')

        if to_fields is None:
                # If to_fields is not given, we have no choice but getting the
                # keywords by inspecting the view. Convenient, but less than
                # ideal, as it means that *args, **kwargs style views signature
                # will not get properly detected -- this is what might happens
                # with views having cascading decorators.
                modelsfields = inspect.getargspec(func)[0][1:]
        else:
            # Other sequences and mappings only needs to be saved, as it's
            # assumed there is a perfect relationship to model fields.
            modelfields = list(to_fields)

        if len(modelfields) == 0:
            raise ValueError(
                'there is no field left to match model entities against: '
                'if all you are interested in is invalidating all pages '
                'associated with a given view whenever an entity '
                'from a given model is changed, use '
                'the cache_page_for_models() decorator instead')

        def invalidate(sender, instance, signal, *args, **kwargs):
            # Construct the mapping from model instance
            mapping = dict((field, getattr(instance, field))
                           for field in modelfields)

            # Get the corresponding local key, and bump it.
            local_key = get_local_key_from_mapping(mapping, view_name)
            print 'local key', local_key
            bump_local_prefix(local_key)
            print 'Invalidating:', instance, signal, args, kwargs

        post_save.connect(invalidate, sender = model, weak = False,
                          dispatch_uid = view_name)

        return decorator_from_middleware_with_args(
            CacheWithLocalVersionMiddleware)(
            cache_timeout = cache_timeout,
            group = to_fields,
            view_func = func,
            vary_on_view = True)(func)

    return cache_page_against_model_decorator

#-------------------------------------------------------------------------------
def cache_page_against_models(*models, **kwargs):
    def cache_page_against_models_decorator(func):
        view_name = get_view_name(func)

        def invalidate(sender, instance, signal, *args, **kwargs):
            bump_local_prefix(get_local_key_from_mapping({}, view_name))

        for model in models:
            for sig in (post_save, post_delete):
                sig.connect(invalidate, sender = model, weak = False,
                            dispatch_uid = view_name)

        return decorator_from_middleware_with_args(
            CacheWithLocalVersionMiddleware)(
            cache_timeout = kwargs.get('cache_timeout'),
            group = (),
            view_func = func,
            vary_on_view = True)(func)

    return cache_page_against_models_decorator

#-------------------------------------------------------------------------------
