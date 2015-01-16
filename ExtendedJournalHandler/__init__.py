#
from systemd.journal import JournalHandler, send

class ExtendedJournalHandler(JournalHandler):

    def emit(self, record):
        """Write record as journal event.

        MESSAGE is taken from the message provided by the
        user, and PRIORITY, LOGGER, THREAD_NAME,
        CODE_{FILE,LINE,FUNC} fields are appended
        automatically. In addition, record.MESSAGE_ID will be
        used if present.
        """
        try:
                msg = self.format(record)
                pri = self.mapPriority(record.levelno)
                mid = getattr(record, 'MESSAGE_ID', None)
                for key in self._extra:
                    if hasattr(record, key):
                        self._extra[key] = getattr(record, key)
                send(msg,
                     MESSAGE_ID=mid,
                     PRIORITY=format(pri),
                     LOGGER=record.name,
                     THREAD_NAME=record.threadName,
                     CODE_FILE=record.pathname,
                     CODE_LINE=record.lineno,
                     CODE_FUNC=record.funcName,
                     **dict((k, v) for k, v in self._extra.iteritems() if v))
        except Exception:
                self.handleError(record)