#!/usr/bin/env python3
import re
import sys

# TODO: rewrite in bash

# add title attribute to img tags
filename = sys.argv[1]
with open(filename, 'r+') as f:
    contents = ''.join(f.readlines())
    regexp = re.compile('alt="(.*?)"')
    # set title to same as alt text
    for match in regexp.finditer(contents):
        contents = contents.replace(
            match.group(0), f'title="{match.group(1)}" {match.group(0)}'
        )

    regexp = re.compile('<figure>.*?(<img.*?/>).*?</figure>', re.DOTALL)
    for match in regexp.finditer(contents):
        contents = contents.replace(match.group(0), match.group(1))


with open(filename, 'wt') as f:
    f.write(contents)
