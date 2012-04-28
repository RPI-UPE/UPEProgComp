import datetime
from collections import defaultdict

units = ['', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year']
conv_sec = [0, 1, 60, 3600, 3600*24, 3600*24*7, 3600*24*30, 3600*24*365]
u_rev = dict((y, x) for x, y in enumerate(units))

# Use a class-as-function-dict
def asdict(cls):
    return cls.__dict__
@asdict
class time_formats:
    def lang(parsed, past):
        if len(parsed) == 0:
            return "just now"

        outs = []
        for unit, count in reversed(parsed.items()):
            if count > 0:
                outs.append("%d %s" % (count, units[unit] + (count != 1 and "s" or "")))
        output = ", ".join(outs)

        if past:
            return output + " ago"
        else:
            return "in " + output

    def decimal(parsed, past=None):
        if len(parsed) == 0:
            return "0:00"

        # Bigger units
        output = []
        for unit in range(u_rev['year'], u_rev['hour'], -1):
            if unit in parsed:
                output.append("%d%s" % (parsed[unit], units[unit][0]))

        # Time
        if u_rev['second'] not in parsed:
            output.append("%d:%02d" % (parsed[u_rev['hour']], parsed[u_rev['minute']]))
        elif u_rev['hour'] not in parsed and len(output) == 0:
            output.append("%d:%02d" % (parsed[u_rev['minute']], parsed[u_rev['second']]))
        else:
            output.append("%d:%02d:%02d" % (parsed[u_rev['hour']], parsed[u_rev['minute']], parsed[u_rev['second']]))

        return " ".join(output)

def relative_time(dt, reftime=None, format='lang', resolution='', convert=1):
    """
    Returns a string to describe the relative time to the given value
    Expects: datetime() object
    Optional Arguments:
        reference   datetime    Use as a reference time. Default now().
        format      str         Expects either decimal ('2:34') or
                                lang ('2 minutes, 34 seconds'). Default lang.
        resolution  str         In the form of [MIN][:MAX], both expect one     |
                                of 'day', 'hour', 'minute', 'second',
                                'microsecond'. Will show at least and/or
                                at most time in that resolution. Default empty.
        convert     int         How many of a time unit you need before you can
                                use this unit. Ex: 1 hour(convert=1) vs 61 minutes
                                (convert=2). Default 1.
    """
    if reftime == None:
        reftime = datetime.datetime.now()
    # Parse resolution
    if ':' in resolution:
        res_min, res_max = resolution.split(':')
    else:
        res_min, res_max = resolution, None
    # Convert to index of unit
    try:
        res_min = res_min and units.index(res_min) or 0
        res_max = res_max and units.index(res_max) or len(units) - 1
    except ValueError:
        raise Exception("Invalid time unit(s): '%s'" % resolution)
    if format == 'decimal': res_min = res_min or u_rev['second']
    # Check convert
    if convert < 1:
        raise Exception("Conversion ratio must be positive (got %d)" % convert)

    # Calculate difference
    if dt > reftime:
        diff = dt - reftime
        past = False
    else:
        diff = reftime - dt
        past = True
    seconds = diff.seconds + diff.days * 24 * 3600
    o_sec = seconds

    # Convert seconds into time components
    parsed = defaultdict(int)

    # Start at the top and work backwards
    for i in range(res_max, res_min-1, -1):
        if i <= 0:
            break
        if seconds >= conv_sec[i] * convert:
            #print "\t %d seconds -> %d seconds (%d %s(s))" % (seconds, (seconds % conv_sec[i]), (seconds / conv_sec[i]), units[i])
            parsed[i] = seconds / conv_sec[i]
            seconds = seconds % conv_sec[i]
            # If we didn't specify a min, we only take one unit
            if not res_min:
                break
        elif len(parsed) > 0:
            parsed[i] = 0

    # Format parsed time and return
    if format in time_formats:
        output = time_formats[format](parsed, past)
    else:
        raise Exception("Invalid format: '%s'" % format)

    return output

if __name__ == '__main__':
    from datetime import timedelta as td
    now = datetime.datetime.now()
    # Test now
    print relative_time(now)
    # Test relative time
    print relative_time(now + td(hours=1), reftime=now - td(hours=1))
    # Test past/future
    print relative_time(now - td(hours=1))
    print relative_time(now + td(hours=1))
    # Test convert
    print relative_time(now + td(hours=1), convert=2)
    print relative_time(now + td(hours=1), convert=61)
    # Test min/max
    print relative_time(now + td(hours=1, minutes=1, seconds=1))
    print relative_time(now + td(hours=1, minutes=1, seconds=1), resolution='second:')
    print relative_time(now + td(hours=1, minutes=1, seconds=1), resolution='second:minute')
    print relative_time(now + td(hours=1, minutes=1, seconds=1), resolution=':minute')
    print relative_time(now + td(seconds=1), resolution=':minute')
    print relative_time(now + td(hours=1), resolution=':second')
    print relative_time(now + td(hours=1), resolution='second:')
    # Test in decimal format
    print relative_time(now, format='decimal')
    print relative_time(now + td(hours=1), format='decimal')
    print relative_time(now + td(hours=1, minutes=20, seconds=45), format='decimal')
    print relative_time(now + td(minutes=20, seconds=45), format='decimal')
    print relative_time(now + td(days=40, hours=1, minutes=20, seconds=45), format='decimal')
