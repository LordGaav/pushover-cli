#
# Copyright (c) 2017 Nick Douma
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from argparse import ArgumentTypeError
from datetime import datetime
from notification_scripts import slack, pushover
import nose.tools


ISO8601_TIMESTAMPS = [
    ("2016-01-01T11:22:33", datetime(2016, 1, 1, 11, 22, 33).timestamp(),
     None),
    ("20160101T11:22:33", datetime(2016, 1, 1, 11, 22, 33).timestamp(), None),
    ("20160101 112233", datetime(2016, 1, 1, 11, 22, 33).timestamp(), None),
    ("20160101112233", datetime(2016, 1, 1, 11, 22, 33).timestamp(), None),
    ("123", 123, None),

    (345, 345, TypeError),  # Must supply a string
    ("2016-1-1T11:22:33", None, ArgumentTypeError),  # Invalid month / day
]


def _test_iso8601_timestamp(func, _in, _out, _sideeffect):
    if _sideeffect:
        with nose.tools.assert_raises(_sideeffect):
            func(_in)
    else:
        nose.tools.assert_equal(func(_in), _out)


def test_iso8601_timestamps_slack():
    for _in, _out, _sideeffect in ISO8601_TIMESTAMPS:
        yield _test_iso8601_timestamp, slack.iso8601_to_unix_timestamp, \
            _in, _out, _sideeffect


def test_iso8601_timestamps_pushover():
    for _in, _out, _sideeffect in ISO8601_TIMESTAMPS:
        yield _test_iso8601_timestamp, pushover.iso8601_to_unix_timestamp, \
            _in, _out, _sideeffect
