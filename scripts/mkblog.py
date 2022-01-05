#!/usr/bin/env python

import os
import sys
import markdown
import re

#   SRC
#   +-2022/
#   | +-10/
#   | +-12/
#   |   +-25/
#   +-2023/
#   | +-1/
#   |   +-26/
#   | +-3/
#   ... 

def print_usage():
    print("\nusage: python mkblog.py SRC DEST\n")
    print("\n")
    print("\t\tSRC\tinput markdown file")
    print("\t\tDEST\tdestination html file")

# check args
if len(sys.argv) != 3:
    print_usage()
    sys.exit(1)

src_file = sys.argv[1]
dest_file = sys.argv[2]

# check blog root exists
if not os.path.isfile(src_file):
    print("{blog_root} doesn't exist")
    sys.exit(1)

# make dest dir if it doesnt exist

dest_dir = os.path.dirname(dest_file)
print(dest_dir)
if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

# write markdown into a dummy file first so that we can add lines before it in the final output
dummy_file = f"{dest_file}.bak"
open(dummy_file, 'w').close()

print(f"{dummy_file} -> {dummy_file}")
markdown.markdownFromFile(input=src_file, output=dummy_file, extensions=["fenced_code"])

print(f"{dummy_file} -> {dest_file}")
with open(dummy_file, 'r') as read_file, open(dest_file, 'w') as write_file:
    write_file.write("#include blogstart.html\n")

    # modify the basic html to make it nicer for styling later
    html = read_file.read()

    # insert text-panel start between non-<p> and <p> elements
    html = re.sub('((?<!</p>)\n)(<p>)', r'\1<div class="text-panel">\n\2', html)
    # insert para-block end between <p> and non-<p> elements
    html = re.sub('(</p>\n)((?!<p>))', r'\1</div>\n\2', html)

    # insert code-panel start before <pre> elements
    html = re.sub('(<pre>)', r'<div class="code-panel">\n\1', html)
    # insert code-panel end after </pre> elements
    html = re.sub('(</pre>)', r'\1\n</div>', html)

    # replace horizontal rules with nice separator dot
    html = re.sub('<hr />', r'<div class="separator"></div>', html)

    lines = html.split("\n")

    # tack on a closing div because we will have opened one without closing it on the final <p>
    lines.append("</div>")

    for line in lines:
        write_file.write(line + "\n")

    write_file.write("\n#include blogend.html\n")

os.remove(dummy_file)


