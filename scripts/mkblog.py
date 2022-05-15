#!/usr/bin/env python

import os
import sys
import markdown

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
    print("\t\SRC\tinput markdown file")
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

print(f"{src_file} -> {dest_file}")
markdown.markdownFromFile(input=src_file, output=dest_file, extensions=["fenced_code"])

