"""
sudo -E env PATH=$PATH python3 main.py
"""

import json
import pathlib

from apachelogs import LogParser, COMBINED

parser = LogParser(COMBINED)

log_path = pathlib.Path("/var/log/apache2/flaskrest-access.log.1")

with open(log_path) as fp:
	for entry in parser.parse_lines(fp):
		print(str(entry.request_time), entry.request_line)
	