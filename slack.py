#!/usr/bin/env python3
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

from argparse import ArgumentParser, ArgumentTypeError
import datetime
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import sys

ISO8601 = r"^(\d{4})-?(\d{2})-?(\d{2})?[T ]?(\d{2}):?(\d{2}):?(\d{2})"


def iso8601_to_unix_timestamp(value):
    try:
        return int(value)
    except ValueError:
        pass
    matches = re.match(ISO8601, value)
    if not matches:
        raise ArgumentTypeError("Argument is not a valid UNIX or ISO8601 "
                                "timestamp.")
    return int(datetime.datetime(
        *[int(m) for m in matches.groups()])).timestamp()


def hex_value(value):
    value = value.replace("#", "")
    if not re.match(r"^[a-f0-9]{6}$", value):
        raise ArgumentTypeError("Argument is not a valid hex value.")
    return value


parser = ArgumentParser(description="Send notifications using Slack")
parser.add_argument("--webhook-url", help="Webhook URL.", required=True)
parser.add_argument("--channel", help="Channel to post to (prefixed with #), "
                    "or a specific user (prefixed with @).")
parser.add_argument("--username", help="Username to post as")
parser.add_argument("--title", help="Notification title.")
parser.add_argument("--title_link", help="Notification title link.")
parser.add_argument("--color", help="Sidebar color (as a hex value).",
                    type=hex_value)
parser.add_argument("--ts", help="Unix timestamp or ISO8601 timestamp "
                    "(will be converted to Unix timestamp).",
                    type=iso8601_to_unix_timestamp)
parser.add_argument("message", help="Notification message.")

args = parser.parse_args()

message = {}

for param in ["channel", "username"]:
    value = getattr(args, param)
    if value:
        message[param] = value

attachment = {}
for param in ["title", "title_link", "color", "ts", "message"]:
    value = getattr(args, param)
    if value:
        attachment[param] = value
attachment['fallback'] = attachment['message']
attachment['text'] = attachment['message']
del attachment['message']

message['attachments'] = [attachment]

payload = {"payload": json.dumps(message)}

try:
    parameters = urllib.parse.urlencode(payload).encode('UTF-8')
    url = urllib.request.Request(args.webhook_url, parameters)
    responseData = urllib.request.urlopen(url).read()
except urllib.error.HTTPError as he:
    print("Sending message to Slack failed: {}".format(he))
    sys.exit(1)
