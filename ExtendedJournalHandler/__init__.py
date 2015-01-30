from systemd.journal import JournalHandler, send

JOURNAL_KEY_PREFIX = "JOURNAL_"

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
                extra = dict(self._extra)
                for key in record.__dict__:
                    if key.startswith(JOURNAL_KEY_PREFIX):
                        extra[key[len(JOURNAL_KEY_PREFIX):]] = getattr(record, key)
                send(msg,
                     MESSAGE_ID=mid,
                     PRIORITY=format(pri),
                     LOGGER=record.name,
                     THREAD_NAME=record.threadName,
                     CODE_FILE=record.pathname,
                     CODE_LINE=record.lineno,
                     CODE_FUNC=record.funcName,
                     **extra)
        except Exception:
                self.handleError(record)