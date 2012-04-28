import datetime
from django.template import Library
from progcomp.templatetags.relative_time_format import relative_time as formatter

register = Library()

# General purpose tag
@register.simple_tag
def relative_time(dt, reftime=None, format='lang', resolution='', convert=1):
    return formatter(dt, reftime, format, resolution, convert)

# Short times in decimal display, such as how long it took to complete a problem, etc.
@register.filter
def decimal_time(dt, reftime=None):
    return formatter(dt, reftime, format='decimal')

# Relative times with more unit resolution
@register.filter
def clear_time(dt, reftime=None):
    return formatter(dt, reftime, convert=2)
