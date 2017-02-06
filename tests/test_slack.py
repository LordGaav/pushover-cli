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
from notification_scripts import slack
import nose.tools

HEX_VALUES = [
    ("000000", "000000", None),
    ("#000000", "000000", None),
    ("#abcdef", "abcdef", None),
    (000000, None, AttributeError),  # Must supply a string
    ("000", None, ArgumentTypeError),  # Must be six characters long
    ("bcdefg", None, ArgumentTypeError)  # Must contain only hexadecimal chars
]


def _test_hex_value(_in, _out, _sideeffect):
    if _sideeffect:
        with nose.tools.assert_raises(_sideeffect):
            slack.hex_value(_in)
    else:
        nose.tools.assert_equal(slack.hex_value(_in), _out)


def test_hex_values():
    for _in, _out, _sideeffect in HEX_VALUES:
        yield _test_hex_value, _in, _out, _sideeffect
