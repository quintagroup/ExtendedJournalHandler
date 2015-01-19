# ExtendedJournalHandler
Python logging handler extending functionality of basic journal handler from python-systemd.

To create a custom logger whose messages go only to journal use:

```
>>> from ExtendedJournalHandler import ExtendedJournalHandler
>>> log = logging.getLogger('custom_logger_name')
>>> log.propagate = False
>>> log.addHandler(journal.ExtendedJournalHandler())
>>> log.warn("Some message: %s", detail)
```

ExtendedJournalHandler extends JournalHandler from [python-systemd package] (http://www.freedesktop.org/software/systemd/python-systemd/journal.html#journalhandler-class).


To attach journal extra keys add "JOURNAL_" prefix to the key title. For example:

```
>>> import uuid
>>> value = uuid.UUID('0123456789ABCDEF0123456789ABCDEF')
>>> log.warn("Message with MY_KEY", extra={'JOURNAL_MY_KEY': value})
```

The MY_KEY field will be sent to journal.

