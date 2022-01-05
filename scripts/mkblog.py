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

with open(src_file) as md:

    dest_dir = os.path.dirname(dest_file)
    print(dest_dir)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_file, "w") as html:

        print(f"{src_file} -> {dest_file}")
        html.write(markdown.markdown(md.read()))

#for dir_y in os.listdir(src_dir):
#    path_y = os.path.join(src_dir, dir_y)
#
#    if not os.path.isdir(path_y):
#        continue
#
#    for dir_m in os.listdir(path_y):
#        path_m = os.path.join(path_y, dir_m)
#
#        if not os.path.isdir(path_m):
#            continue
#
#        for dir_d in os.listdir(path_m):
#            path_d = os.path.join(path_m, dir_d)
#
#            if not os.path.isdir(path_d):
#                continue
#
#            print(path_d)
#            for md in os.listdir(path_d):
#                path_md = os.path.join(path_d, md)
#
#                if not os.path.isfile(path_md):
#                    continue


