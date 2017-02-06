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
import re
import urllib.error
import urllib.parse
import urllib.request
import sys

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

SOUNDS = [
    "pushover",
    "bike",
    "bugle",
    "cashregister",
    "classical",
    "cosmic",
    "falling",
    "gamelan",
    "incoming",
    "intermission",
    "magic",
    "mechanical",
    "pianobar",
    "siren",
    "spacealarm",
    "tugboat",
    "alien",  # Long sounds from here
    "climb",
    "persistent",
    "echo",
    "updown",
    "none"  # No sound
]
LEVELS = [-2, -1, 0, 1, 2]

ISO8601 = r"^(\d{4})-?(\d{2})-?(\d{2})?[T ]?(\d{2}):?(\d{2}):?(\d{2})"


def iso8601_to_unix_timestamp(value):
    matches = re.match(ISO8601, value)
    if matches:
        return int(datetime.datetime(
            *[int(m) for m in matches.groups()]).timestamp())

    try:
        return int(value)
    except ValueError:
        raise ArgumentTypeError("Argument is not a valid UNIX or ISO8601 "
                                "timestamp.")


def arguments():
    parser = ArgumentParser(description="Send notifications using Pushover")
    parser.add_argument("--token", help="Application token.", required=True)
    parser.add_argument("--user", help="User destination token.",
                        required=True)
    parser.add_argument("--device", help="Device name to target specifically, "
                        "may contain more than one separated by comma's.")
    parser.add_argument("--title", help="Notification title.")
    parser.add_argument("--sound", help="Play a specific sound.",
                        choices=SOUNDS)
    parser.add_argument("--priority", help="Notification priority.", type=int,
                        choices=LEVELS, default=0)
    parser.add_argument("--url", help="Supplementary URL.")
    parser.add_argument("--url_title", help="Supplementary URL title.")
    parser.add_argument("--timestamp", help="Unix timestamp or ISO8601 "
                        "timestamp (will be converted to Unix timestamp).",
                        type=iso8601_to_unix_timestamp)
    parser.add_argument("--retry", help="Retry message every x seconds. Only "
                        "used when priority is 2.", type=int, default=30)
    parser.add_argument("--expire", help="Expire message after x seconds. "
                        "Only used when priority is 2.", type=int, default=300)
    parser.add_argument("message", help="Notification message.")

    args = parser.parse_args()

    if args.retry < 30:
        args.retry = 30

    return args


def format_payload(args):
    parameters = {}
    for param, value in vars(args).items():
        if value:
            parameters[param] = value
    payload = urllib.parse.urlencode(parameters).encode('UTF-8')
    return payload


def send_message(payload):
    try:
        url = urllib.request.Request(PUSHOVER_URL, payload)
        urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as he:
        print("Sending message to Pushover failed: {}".format(he))
        sys.exit(1)


def main():
    args = arguments()
    payload = format_payload(args)
    send_message(payload)


if __name__ == "__main__":
    main()
