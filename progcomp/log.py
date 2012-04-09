import datetime
import logging
import traceback

from settings import LOG_FILE

class ErrorHandler(logging.Handler):
    def emit(self, record):
        with open(LOG_FILE, "a+") as logfile:
            timestamp = datetime.datetime.fromtimestamp(record.created).strftime("%d/%b/%Y %H:%M:%S")
            query = "%s %s %s" % (record.request.META['REQUEST_METHOD'], record.request.META['PATH_INFO'], record.request.META['SERVER_PROTOCOL'])
            logfile.write('[%s] "%s" %d\n' % (timestamp, query, record.status_code))
            traceback.print_exception(*record.exc_info, file=logfile)
            logfile.write("\n\n")
