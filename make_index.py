#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

"""
make index json file from text file tree.
Expects Python 3

https://github.com/sukuba/js-py-document-search
"""

import argparse
import os
import shutil
import datetime

import jsngram.jsngram
import jsngram.dir2

def remove_entries(dest):
    """
    remove files and subdirectories at dest
    """
    for entry in os.listdir(dest):
        fullpath = os.path.join(dest, entry)
        if os.path.isfile(fullpath):
            os.remove(fullpath)
        else:
            shutil.rmtree(fullpath)
    
def make_index_by_files_inc(n, shorter, src, dest, flat, ignore, files_at_once, verbose_print):
    """
    text files in src directory will be indexed.
    """
    ix = jsngram.jsngram.JsNgram(n, shorter, src, dest, flat, ignore)
    entries = jsngram.dir2.list_files(src)
    n = len(entries)
    for files in (entries[i:i+files_at_once] for i in range(0, n, files_at_once)):
        ix.add_files_to_json(files, verbose_print)
        print('%d indexes in %d files' % (len(ix.db), len(files)))
        for f in files:
            print(' ' + f)
    print('%d files processed.' % len(entries))
    return ix
    
def make_index(args):
    """
    make index json file from text file tree
    expected args; src, dest, size, noshorter, flat, once, ignore, verbose
    """
    start_time = datetime.datetime.now()
    print('Start: ', start_time)
    
    print('Removing current index files ...')
    remove_entries(args.dest)
    
    print('Building index files ...')
    ix = make_index_by_files_inc(args.size, not args.noshorter, args.src, args.dest,
                                 args.flat, args.ignore, args.once, args.verbose)
    
    print('Adjusting index files ...')
    entries = jsngram.dir2.list_files(args.dest)
    for entry in entries:
        fullpath = os.path.join(args.dest, entry)
        jsngram.json2.json_end(fullpath)
    print('%d indexes' % len(entries))
    
    print('Done.')
    
    end_time = datetime.datetime.now()
    span = end_time - start_time
    sspan = '%d seconds' % span.seconds if span.seconds < 3600 else '%d hours' % (span.days * 24)
    print('End: ', end_time, ' / runtime: ', sspan)
    

def main():
    r"""
    正規化済みのテキスト群からインデックスファイルを作る。
    
    make_index.py E:\scratch txt idx
    
    第1引数: 基準ディレクトリ（フルパス）
    第2引数: 変換元テキストディレクトリ（基準からの相対パス）
    第3引数: インデックス出力先ディレクトリ（基準からの相対パス）
    --size: N-gramの文字長（デフォルト 2）
    --noshorter: 文字長より短いインデックスは作成しない（デフォルト False）
    --flat: ディレクトリ型でなく、ファイル型のインデックスを作成する（デフォルト False）
    --once: 一度にインデックスを作成するファイル数（デフォルト 100）
    --ignore: 単語区切りとして、インデックスから除外する文字パターン（正規表現; デフォルト [\s,.，．、。]+）
    --verbose: 冗長な情報を出力する
    
    入力は、単一ディレクトリ配下にtree構造で配置された、正規化済みの utf-8 text ファイル群。
    出力は、N-gramによりtree構造に作成したインデックスファイル群。
    
    """
    parser = argparse.ArgumentParser(description='正規化済みのテキスト群からインデックスファイルを作る')
    parser.add_argument('base', help='基準ディレクトリ（フルパス）')
    parser.add_argument('src', help='変換元テキストディレクトリ（基準からの相対パス）')
    parser.add_argument('dest', help='インデックス出力先ディレクトリ（基準からの相対パス）')
    parser.add_argument('-s', '--size', type=int, default=2, help='N-gramの文字長')
    parser.add_argument('-n', '--noshorter', action='store_true', help='文字長より短いインデックスは作成しない')
    parser.add_argument('-f', '--flat', action='store_true', help='ディレクトリ型でなく、ファイル型のインデックスを作成する')
    parser.add_argument('-o', '--once', type=int, default=100, help='一度にインデックスを作成するファイル数')
    parser.add_argument('-i', '--ignore', type=str, default=r'[\s,.，．、。]+', help='単語区切りとして、インデックスから除外する文字パターン')
    parser.add_argument('-v', '--verbose', action='store_true', help='冗長な情報を出力する')
    args = parser.parse_args()
    
    args.src = os.path.join(args.base, args.src)
    args.dest = os.path.join(args.base, args.dest)
    
    if args.verbose:
        print(args)
    make_index(args)

if __name__ == '__main__':
    main()
