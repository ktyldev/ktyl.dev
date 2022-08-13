#!/usr/bin/env python3

import sys
import re

# we expect the arguments to be filepaths to each blog post

def print_usage():
    print("\nusage: python mkblogindex.py POSTS\n")
    print("\n")
    print("\t\tPOSTS\tfilepaths of blog posts")

# check args for at least one file path
if len(sys.argv) < 2:
    print_usage()
    sys.exit(1)

# posts are arguments from index 1 onwards
posts = sys.argv[1:]

dir_pattern = re.compile("(.+)/(blog\/.+\.html)")
path_pattern = re.compile("(.+)\/(\d{4})\/(\d{1,2})\/(\d{1,2})\/(.+).html")
title_pattern = re.compile("<h1>(.+)</h1>")

# filter posts to just those with a date in them
posts = [p for p in posts if path_pattern.match(p)]
posts.reverse()

links = []

# for each file we want to output an <a> tag with a relative href to the site root
for path in posts:
    m = re.match(path_pattern, path)
    year = m.group(2)
    month = m.group(3).rjust(2, '0')
    day = m.group(4).rjust(2, '0')

    date = f'<span class="post-date">{year}-{month}-{day}</span>'

    title = ""
    with open(path) as f:
        for line in f:
            if title_pattern.match(line):
                title = re.sub(title_pattern, r'<span class="post-title">\1</span>', line).strip()
                break

    # clean leading directories to get the relative path we'll use for the link
    url = re.sub(dir_pattern, r"\2", path)

    item = (date, f'<li><a href="{url}">{date}{title}</a></li>')
    links.append(item)

# make sure we're properly ordered in reverse date order lol
links = sorted(links, key=lambda x: x[0])
links.reverse()

for l in links:
    print(l[1])

