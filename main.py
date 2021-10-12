#!venv/bin/python
"""
sudo -E env PATH=$PATH python3 main.py
"""

import json
import pathlib
from urllib import request, parse



from apachelogs import LogParser

parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")

log_path = pathlib.Path("/var/log/apache2/flaskrest-access.log.1")

entries = []

with open(log_path) as fp:
	for entry in parser.parse_lines(fp):
		entries.append({
			"remote_host": entry.remote_host,
			"time": str(entry.request_time_fields["timestamp"]),
			"request": entry.request_line,
			"status": entry.final_status,
			"referer": entry.headers_in["Referer"],
			"user_agent": entry.headers_in["User-Agent"]
		})
		

payload =json.dumps({"data":entries}).encode("utf-8")

req = request.Request(
	"https://script.google.com/macros/s/AKfycbyz-M41gShgHcK8Lkw9UGsid2WYU93O7zA6tnmFY0qvQEa2282jZA5C6FWeLI2D-Hh2/exec?path=serverLogs",
	headers={"Content-type": "text/plain"}
	)
	
resp = request.urlopen(req, data=payload)
	
print(resp.read())

