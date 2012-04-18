"""
Low-level utilities to deal with generational caching.

Usual way to deal with the cache is this: you compute a key, and you
try to retrieve an item using it. Here, we add a single level of
indirection: you compute a first key out of a group definition and
keyworded values: it's the local key. You then fetch the value for it:
it's the so-called local version/generation. Finally, you use this version
to construct the 'real' key presumably associated with the cache item
you are ultimately after.

The strong point of this technique is that you can selectively
invalidate a custom group of keys sharing a version in a single sweep
just by bumping the version.

Given a group, view keywords, and an optional view_name. You can:

1) Compute the local key (see get_local_key()). If:

   - group is None, use the hash of the view keywords as local key.

   - group is a string, use a hash of it as local key.

   - group is a callable, it's called with all the view_keywords (as
     keywords), and it's expected to return a mapping of (key, value) pairs. The
     hash of this mapping is the local key.

   - group is a dictionnary specifying how to remap view keywords (from
     new keywords to old keywords). The hash of the remapped keywords is the
     local key.

   - group is a sequence, a new dictionnary is formed from view_keywords
     with only the keys listed in group. The hash of the remaining
     keywords is the local key.

   If a view name is passed along, it's used during hash computation.

2) Use this local key to resolve the local prefix (see get_local_prefix())

3) Invalidate the current local prefix (see bump_local_prefix()).
"""
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor
from django.conf import settings

import logging, random

#-------------------------------------------------------------------------------
logger = logging.getLogger('groupcache')  # Set up an application-level logger

if True:
    import sys
    logger.setLevel(logging.DEBUG)
    _hdlr = logging.StreamHandler(sys.stdout)
    _hdlr.setLevel(logging.DEBUG)
    _hdlr.setFormatter(logging.Formatter(
            '%(asctime)-15s GROUPCACHE (%(levelname)s) %(message)s'))
    logger.addHandler(_hdlr)

#-------------------------------------------------------------------------------
def _join_prefixes(prefixes, terminal = ''):
    return '%s%s' % (
        '.'.join(pfx for pfx in prefixes if pfx is not None and len(pfx) > 0),
        terminal)

def _hash_mapping(mapping, view_name = None):
    ctx = md5_constructor()
    for k, v in sorted(mapping.iteritems()):
        ctx.update(k)
        ctx.update(v)
    if view_name is not None:
        ctx.update(view_name)
    return ctx.hexdigest()

def _get_randval():
    return random.randint(0, 10000)

def _get_key_prefix(key_prefix):
    if key_prefix is None:
        return getattr(settings, 'CACHE_MIDDLEWARE_KEY_PREFIX', '')
    else:
        return key_prefix

#-------------------------------------------------------------------------------
def get_view_name(view_func):
    return '.'.join((view_func.__module__, view_func.__name__))

def get_local_key_mapping(group, view_keywords):
    if group is None:
        mapping = view_keywords
    elif isinstance(group, basestring):
        mapping = {'group': group}
    elif callable(group):
        mapping = group(**view_keywords)
    elif isinstance(group, dict):
        mapping = dict((new, view_keywords[old])
                       for new, old in group.iteritems())
    else:
        mapping = dict((k, view_keywords[k]) for k in group)
    return mapping

def get_local_key_from_mapping(mapping, view_name = None, key_prefix = None):
    return _join_prefixes(
        (_get_key_prefix(key_prefix),
         'local_key',
         _hash_mapping(mapping, view_name)))

def get_local_key(group, view_keywords, view_name = None,
                  key_prefix = None):
    return get_local_key_from_mapping(
        get_local_key_mapping(group, view_keywords),
        view_name, key_prefix)

    return _join_prefixes(
        _get_key_prefix(key_prefix), 'local_key',
        _hash_mapping(get_local_key_mapping(group, view_keywords),
                      view_name))

def bump_local_prefix(local_key):
    try:
        cache.incr(local_key)
        logger.debug(
            'bumping local prefix for local key %s (%s)' % (
                local_key, cache.get(local_key)))
    except ValueError:
        logger.debug(
            'failed bumping local prefix for local_key %s, recreating' %
            local_key)
        cache.add(local_key, _get_randval())

def get_local_prefix(local_key, key_prefix = None):
    version = cache.get(local_key)
    #logger.debug('got local prefix for: %s (%s)' % (local_key, version))
    if version is None:
        version = _get_randval()
        cache.set(local_key, version)
    return _join_prefixes((_get_key_prefix(key_prefix), 'local', str(version)),
                          terminal = '.')

#-------------------------------------------------------------------------------
