"""
pytest-winnotify
Windows notify support for py.test
Requirements: pywin32
"""
import time
from winnotify import WinTrayIcon


def pytest_addoption(parser):
    """Adds options to control notifications."""
    group = parser.getgroup('terminal reporting')
    group.addoption('--winnotify',
                    dest='winnotify',
                    default=True,
                    help='Enable Windows notifications.')


def pytest_sessionstart(session):
    if session.config.option.winnotify:
        setattr(session.config, "winnotifier", WinTrayIcon("py.test"))
        assert isinstance(session.config.winnotifier, WinTrayIcon)
        session.config.winnotifier.balloon_tip("py.test", "Running tests...")


def pytest_terminal_summary(terminalreporter):
    if not terminalreporter.config.option.winnotify:
        return
    tr = terminalreporter
    passes = len(tr.stats.get('passed', []))
    fails = len(tr.stats.get('failed', []))
    skips = len(tr.stats.get('deselected', []))
    errors = len(tr.stats.get('error', []))
    msgIcon = WinTrayIcon.MSG_INFO
    if errors + passes + fails + skips == 0:
        msg = "No tests ran"
    elif passes and not (fails or errors):
        msg = 'Success - %i Passed' % passes
    elif not (skips or errors):
        msg = "%s Passed %s Failed" % (passes, fails)
        msgIcon = WinTrayIcon.MSG_WARNING
    else:
        msg = "%s Passed %s Failed %s Errors %s Skipped" % (passes, fails, errors, skips)
        msgIcon = WinTrayIcon.MSG_ERROR
    assert isinstance(terminalreporter.config.winnotifier, WinTrayIcon)
    terminalreporter.config.winnotifier.balloon_tip("py.test", msg, icon=msgIcon)
