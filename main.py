#!venv/bin/python
"""
sudo -E env PATH=$PATH python3 main.py
"""

import json
import pathlib

from apachelogs import LogParser

parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")

log_path = pathlib.Path("/var/log/apache2/flaskrest-access.log.1")

with open(log_path) as fp:
	for entry in parser.parse_lines(fp):
		print(
			entry.remote_host,
			entry.request_time_fields["timestamp"],
			entry.request_line,
			entry.final_status,
			entry.headers_in["Referer"],
			entry.headers_in["User-Agent"]
		)