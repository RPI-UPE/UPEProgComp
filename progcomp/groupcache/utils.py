from django.core.urlresolvers import resolve, reverse

from groupcache.core import logger, \
    get_view_name, get_local_key, bump_local_prefix

#-------------------------------------------------------------------------------
_bumping_cache = {} # Maps view names to their group and vary on view

#-------------------------------------------------------------------------------
def _uncache(view_name, view_keywords):
    # Retrieve the local versioning parameters, build the local version, then
    # bump it.
    try:
        group, vary_on_view = _bumping_cache[view_name]
    except KeyError:
        raise ValueError(
            'view %s was not found in local versionning cache' % view_name)
    bump_local_prefix(
        get_local_key(group, view_keywords,
                      view_name if vary_on_view is True else None))

def uncache(view_name, **view_keywords):
    '''Remove from cache a locally-versionned view call'''
    # We call reverse() to be sure the view is constructed, and the view cache
    # properly populated in the current instance.
    # (TODO: check more closely if it's really needed)
    reverse(view_name, args = (), kwargs = view_keywords)
    _uncache(view_name, view_keywords)

def uncache_from_path(path):
    '''Remove from cache a locally-versionned view call based on it\'s path'''
    view, args, view_keywords = resolve(path)
    assert(len(args) == 0)
    logger.debug('uncaching path: %s' % path)
    _uncache(get_view_name(view), view_keywords)

def uncache_from_tag(tag):
    '''Companion to groupcache.decorators.cache_tagged_page'''
    logger.debug('uncaching tag: %s' % tag)
    bump_local_prefix(get_local_key(tag, {}, None))
