try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO  # NOQA
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # NOQA
try:
    from unittest import main, skip, skipIf, TestCase, TestSuite, findTestCases
except ImportError:
    from unittest2 import skip, skipIf, TestCase, TestSuite  # NOQA
    from unittest2 import findTestCases  # NOQA
from circus.util import IS_WINDOWS
import os
import tempfile
import subprocess
import sys
from systemd import journal
from datetime import timedelta, datetime


HERE = os.path.abspath(os.path.dirname(__file__))
cfg_path = os.path.join(HERE, 'circus.ini')

python = '/data/leits/circus_logging/bin/python'


def run_circusd(config=()):
    temp_dir = tempfile.mkdtemp()
    config_ini = ConfigParser()
    config_ini.read(config)
    circus_ini_path = os.path.join(temp_dir, "circus.ini")
    with open(circus_ini_path, "w") as fh:
        config_ini.write(fh)
    env = os.environ.copy()
    argv = ["circus.circusd"] + [circus_ini_path]
    if sys.gettrace() is None or IS_WINDOWS:
        argv = [python, "-m"] + argv
    else:
        exe_dir = os.path.dirname(python)
        coverage = os.path.join(exe_dir, "coverage")
        if not os.path.isfile(coverage):
            coverage = "coverage"
        argv = [coverage, "run", "-p", "-m"] + argv
    child = subprocess.Popen(argv, cwd=temp_dir, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             env=env)
    pid = child.pid
    log_msg = "[INFO] circus_logger started"

    while True:
        if log_msg in child.stdout.readline():
            break
    child.kill()

    return pid


class TestLogging(TestCase):

    def test_circus_journal_logger(self):
        log_msg = 'Circus journal logger test'
        j = journal.Reader()
        j.seek_realtime(datetime.now() - timedelta(minutes=1))
        pid = run_circusd(config=cfg_path)
        j.add_match(_PID=pid)
        for entry in j:
            self.assertTrue(log_msg in entry['MESSAGE'], entry)
            self.assertTrue(log_msg in entry['INIT_TEST'], entry)
        j.close()


if __name__ == '__main__':
    main()
