#!/usr/bin/env python3

import markdown
import pathlib
import sys
import re

def print_usage():
    print("\nusage: python mkblogrss.py POSTS\n")
    print("\n")
    print("\t\tPOSTS\tfilepaths of blog posts")

# check args for at least one file path
if len(sys.argv) < 2:
    print_usage()
    sys.exit(1)
    
# posts are arguments from index 1 onwards
posts = sys.argv[1:]

# header and footer to enclose feed items
header = """<?xml version="1.0" encoding="utf-8" ?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
    <title>ktyl.dev</title>
    <link>https://ktyl.dev/blog/index.html</link>
    <description>mostly computer stuff!</description>
    <atom:link href="https://ktyl.dev/blog/index.xml" rel="self" type="application/rss+xml"/>
    """
footer = "</channel></rss>"

# regex patterns
title_pattern = re.compile("<h1>(.+)</h1>")
path_pattern = re.compile("(.+)\/(\d{4})\/(\d{1,2})\/(\d{1,2})\/(.+).md")

def make_item(path):
    str = "<item>\n"

    # get the HTML version of the file
    text = ""
    with open(path) as f:
        text = f.read()
    html = markdown.markdown(text, extensions=["fenced_code"])

    # title
    title = ""
    m = title_pattern.match(html)
    title = m.group(1)
    str += f"<title>{title}</title>\n"

    # link
    url = "/".join(pathlib.Path(path).parts[2:])
    url = url.replace(".md", ".html")
    link = f"https://ktyl.dev/blog/{url}"
    str += f"<link>{link}</link>\n"

    # content
    description = html
    description = re.sub('<', '&lt;', description)
    description = re.sub('>', '&gt;', description)
    str += f"<description>{description}</description>\n"

    # pub date
    date = re.sub(path_pattern, r'\2-\3-\4', path)
    str += f"<pubDate>{date}</pubDate>\n"

    str += "</item>"

    return str

# print everything!
print(header)
for p in posts:
    print(make_item(p))
print(footer)

