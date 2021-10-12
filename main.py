import json
import pathlib

log_path = pathlib.Path("/var/log/apache2/flaskrest-access.log.1")

contents = log_path.read_text()

lines = contents.split("\n")

for i, l in enumerate(lines):
	parts = l.split(" ")
	for j, p in enumerate(parts):
		print(i, j, p)