#!/usr/bin/env python

"""
Convert json file from Excel (Nested Array) into Hashed json file for fileinfo.
Expects Python 3

https://github.com/sukuba/js-py-document-search
"""

import argparse
import os.path
import codecs
import json
import re

def make_fileinfo(args):
    """
    Convert json file from Excel (Nested Array) into Hashed json file for fileinfo.
    expected args; src, dest, key, value, convertbackslash
    """
    with codecs.open(args.src, 'r', 'utf-8') as infile:
        data = json.load(infile)
        
    push_all = not args.value
    conv = re.compile(r'\\')
    bag = {}
    for x in data:
        k = x[args.key]
        if not k:
            continue
        if args.convertbackslash:
            k = conv.sub('/', k)
        if push_all:
            bag[k] = x
        else:
            bag[k] = []
            for i in args.value:
                bag[k].append(x[i])
        
    with codecs.open(args.dest, 'w', 'utf-8') as outfile:
        json.dump(bag, outfile, ensure_ascii=False, indent=2)
    

def main():
    r"""
    jsonファイルをfileinfo用に変換する。
    
    make_fileinfo.py E:\scratch\sheet1.json E:\scratch\fileinfo.json --key 6 --value 4 5 1 2 3 0 --convertbackslash
    
    第1引数: 変換元jsonファイル（フルパス）
    第2引数: 出力先jsonファイル（フルパス）
    --key: keyとする項目（0からの序数）
    --value: valueのArrayに入れる項目（0からの序数、複数）
    --convertbackslash: key項目のバックスラッシュをスラッシュに変換する
    --verbose: 冗長な情報を出力する
    
    入力元:
    ArrayのArray
    
    出力:
    value=ArrayなHash
    
    ディレクトリは自動で作らない。
    
    """
    parser = argparse.ArgumentParser(description='jsonファイルをfileinfo用に変換する')
    parser.add_argument('src', help='変換元jsonファイル')
    parser.add_argument('dest', help='出力先jsonファイル')
    parser.add_argument('-k', '--key', type=int, default=0, help='keyとする項目（0からの序数）')
    parser.add_argument('-a', '--value', type=int, nargs='+', help='keyとする項目（0からの序数）')
    parser.add_argument('-c', '--convertbackslash', action='store_true', help='key項目のバックスラッシュをスラッシュに変換する')
    parser.add_argument('-v', '--verbose', action='store_true', help='冗長な情報を出力する')
    args = parser.parse_args()
    
    if args.verbose:
        print(args)
    make_fileinfo(args)

if __name__ == '__main__':
    main()
