from datetime import timedelta, datetime
import logging
try:
    from unittest import main, TestCase
except ImportError:
    from unittest2 import main, TestCase
from systemd import journal
from ExtendedJournalHandler import ExtendedJournalHandler


class TestLogging(TestCase):

    def test_extended_journal_handler(self):
        log_msg = 'test_extended_journal_handler'
        LOGGER = logging.getLogger()
        LOGGER.setLevel('DEBUG')
        LOGGER.addHandler(ExtendedJournalHandler())
        LOGGER.info("Test extended journal handler",
                    extra={'MESSAGE_ID': log_msg,
                           'JOURNAL_EXTRA': 'foo', 'JOURNAL_ANOTHER_EXTRA': 'bar'})
        j = journal.Reader()
        j.seek_realtime(datetime.now() - timedelta(minutes=3))
        j.add_match(MESSAGE_ID=log_msg)
        for entry in j:
            self.assertTrue(log_msg in entry['MESSAGE_ID'], entry)
            self.assertTrue('EXTRA' in entry, entry['EXTRA'] == 'foo')
            self.assertTrue('ANOTHER_EXTRA' in entry,
                            entry['ANOTHER_EXTRA'] == 'bar')
        j.close()


if __name__ == '__main__':
    main()
