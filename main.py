#!venv/bin/python
"""
sudo -E env PATH=$PATH python3 main.py

55 23 * * * sudo ~/serverLogDump/venv/bin/python3 main.py ~/serverLogDump/

https://script.google.com/home/projects/1hhSmpSflyZEjhhuPTN8u4LMO34E0sx4wzI2ssznRbj9u6vK6dCQlQDy8/edit
"""

import json
import pathlib
from datetime import datetime
from urllib import request

from apachelogs import LogParser

parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")

log_path = pathlib.Path("/var/log/apache2/flaskrest-access.log.1")

entries = []
datetime.today().date()

with open(log_path) as fp:
	for entry in parser.parse_lines(fp):
		if entry.request_time_fields["timestamp"].date() == datetime.today().date():
			entries.append({
				"remote_host": entry.remote_host,
				"time": str(entry.request_time_fields["timestamp"]),
				"request": entry.request_line,
				"status": entry.final_status,
				"referer": entry.headers_in["Referer"],
				"user_agent": entry.headers_in["User-Agent"]
			})
		
if len(entries) > 0:
	payload =json.dumps({"data":entries}).encode("utf-8")

	req = request.Request(
		"https://script.google.com/macros/s/AKfycbyz-M41gShgHcK8Lkw9UGsid2WYU93O7zA6tnmFY0qvQEa2282jZA5C6FWeLI2D-Hh2/exec?path=serverLogs",
		headers={"Content-type": "text/plain"}
		)
		
	resp = request.urlopen(req, data=payload)
		
	print(resp.read())
