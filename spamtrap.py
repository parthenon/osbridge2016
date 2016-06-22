#!/usr/bin/python

import urllib
import re
import sys
import string
import logging
import logging.handlers
from time import strftime

URL="http://blns1.mydomain.com"

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              '/var/log/spam/spamtrap.log', maxBytes=20000, backupCount=5)

my_logger.addHandler(handler)

line = sys.stdin.read()
# The sort of line we get at the top of a mail:
# Received: from hostname.spammer.com (hostname.spammer.com [111.222.123.123])
header = re.search(r'Received: from .*\[([\d\.]+)\]', line)
if header:
    ip = header.group(1)
    my_logger.debug("Reporting IP {} as spam, based on {}".format(ip, header.group(0)))
    f = urllib.urlopen("{}/report/{}".format(URL, ip))

