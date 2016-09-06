#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

"""
List file sizes of specified directory, including subdirectories.
Expects Python 3

https://github.com/sukuba/js-py-document-search
"""

import argparse
import os
import jsngram.dir2

def get_size(src, dummy):
    return os.stat(src).st_size
    
def list_file_size(args):
    """
    List file sizes of source directory, including subdirectories.
    expectes args; src
    """
    result = jsngram.dir2.apply_files(args.src, None, get_size)
    for r in result:
        print('%d\t%s' % (r[2], r[0]))
    

def main():
    r"""
    List file sizes of source directory, including subdirectories.
    
    list-file-size.py E:\scratch\txt
    
    1st arg: Source directory to read files (fullpath)
    
    Output to console: size(bytes) and fullpath delimited with tab
    
    """
    parser = argparse.ArgumentParser(description='List file sizes of source directory')
    parser.add_argument('src', help='Source directory to read files (fullpath)')
    args = parser.parse_args()
    
    list_file_size(args)

if __name__ == '__main__':
    main()
