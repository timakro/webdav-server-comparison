#!/usr/bin/env python3
from collections import defaultdict
import re

# Note: For simplicity we assume litmus output does not contain | or "

paths_and_headers = [
    ('results/apache.txt', 'Apache'),
    ('results/nginx.txt', 'Nginx'),
    ('results/nginx-dav-ext-module.txt', 'Nginx w/ nginx-dav-ext-module'),
    ('results/sabredav.txt', 'Sabre/dav'),
    ('results/sabredav-fsext.txt', 'Sabre/dav w/ FSExt'),
    ('results/lighttpd.txt', 'Lighttpd'),
    ('results/chezdav.txt', 'Chezdav'),
    ('results/rclone.txt', 'Rclone'),
]
paths = [p for p, _ in paths_and_headers]
headers = [h for _, h in paths_and_headers]

table = defaultdict(lambda: defaultdict(lambda: [''] * len(paths)))
for i, path in enumerate(paths):
    with open(path) as file:
        for ln, line in enumerate(file, start=1):
            if m := re.match(r' *[0-9]+\. ([a-z0-9_]+)\.* (.*)', line):
                name, rest = m[1], m[2]
                if m := re.match(r'([a-zA-Z]+):? (.+)', rest):
                    summary, details = m[1], m[2]
                    cell = f'[{summary}]({path}#L{ln} "{details}")'
                else:
                    cell = rest
                table[category][name][i] = cell
            elif m := re.match(r"-> running `(.*)'", line):
                category = m[1]

fmtrow = lambda row: '| ' + ' | '.join(row) + ' |'
print(fmtrow([''] + headers))
print(fmtrow(['---'] * (len(headers) + 1)))
for category, tests in table.items():
    print(fmtrow([f'**{category}**'] + [''] * len(headers)))
    for name, results in tests.items():
        print(fmtrow([name] + results))
