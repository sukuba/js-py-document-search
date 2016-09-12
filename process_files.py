#!/usr/bin/env python

"""
Process files in the full tree of a directory.
Recurses subdirectories excluding dot files and directories.
Uses extra executables to process files.
Expects Python 3

https://github.com/sukuba/js-py-document-search
"""

import subprocess
import sys
import re
import argparse
import codecs
import json
import datetime
import jsngram.dir2

def howto_process(rulefile):
    """
    generate rule function
    """
    try:
        with codecs.open(rulefile, 'r', 'utf-8') as infile:
            rules = json.load(infile)
    except IOError:
        sys.exit('Error: cannot open ' + rulefile)
    except:
        sys.exit('Error: json file maybe collapsed. ' + rulefile)
    print(rules)
    
    def fn_rule(filename, dest):
        com = None
        for rule in rules:
            regexp, command = rule
            if re.search(regexp, filename, re.IGNORECASE):
                com = command
                break
        print(filename, dest, com)
        if com:
            try:
                #subprocess.call([com, filename, dest])
                p = subprocess.Popen([com, filename, dest], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                rc = p.returncode
                print(str(stdout, 'cp932', 'ignore'), str(stderr, 'cp932', 'ignore'), rc)
                return (rc, com, str(stderr, 'utf-8', 'ignore'))
            except OSError as err:
                print(err)
                return (1, com, err)
        return (2, None, None)
    return fn_rule
    
def process_files(args):
    """
    process files in a directory tree at src and write at dest.
    rule is a json file that contains how to process each of files.
    expected args; rule, src, dest, root
    """
    start_time = datetime.datetime.now()
    print('Start: ', start_time)
    
    rule = howto_process(args.rule)
    result = jsngram.dir2.apply_files(args.src, args.dest, rule, not args.root)
    
    end_time = datetime.datetime.now()
    span = end_time - start_time
    sspan = '%d seconds' % span.seconds if span.seconds < 3600 else '%d hours' % span.days * 24
    print('End: ', end_time, ' / runtime: ', sspan)
    
    stat = {'com':{}, 'rc':{}}
    for r in result:
        r_src, r_dest, r_rcs = r
        r_rc, r_com, rc_err = r_rcs
        r_rc_zero = 0 if r_rc == 0 else 1
        stat['com'][r_com] = 1 + stat['com'].get(r_com, 0)
        stat['rc'][r_rc_zero] = 1 + stat['rc'].get(r_rc_zero, 0)
        if r_rc_zero == 1:
            pass
            print('失敗: %s' % r_src)
        
    print('種類別集計: ')
    for k, v in stat['com'].items():
        print('  %d 個を次の手続きで処理。 %s' % (v, k))
    print('全体集計: ')
    print('  %d 個をテキストに変換。' % stat['rc'][0])
    print('  %d 個の変換に失敗。' % stat['rc'][1])
    
    #print(result)
    #print(stat)
    

def main():
    r"""
    サブディレクトリを含めたファイルを変換する。
    
    process_files.py E:\scratch\rule.json E:\scratch\indir E:\scratch\outdir
    
    第1引数: 変換ルールを記述したjsonファイル（フルパス）
    第2引数: 入力元ディレクトリ（フルパス）
    第3引数: 出力先ディレクトリ（フルパス）
    --root: ルートのファイルも出力する
    
    入力元のサブディレクトリを含む全ファイルを、
    変換ルールにしたがって変換し、
    出力先に保存する。
    出力の無いルールでは、出力先は利用しない。
    
    ルール記載例:
    [
      ["\\.txt$", "text-converter.exe"],
      ["\\.(?:doc[mx]?|rtf)$", "word-converter.exe"],
      ["\\.xls$", null],
      [".*", "all-converter.exe"]
    ]
    上から順に適用し、最初の1つだけを適用する。
    1つのルールは、ファイル名と比較する正規表現と、変換プログラムの配列。
    変換をスキップする場合、プログラムに null を指定する。
    最後まで合致するルールが無い場合も、変換をスキップする。
    変換プログラムは、変換元ファイル名と、変換先ディレクトリを受け取る。
    
    """
    parser = argparse.ArgumentParser(description='サブディレクトリを含めたファイルを変換する')
    parser.add_argument('rule', help='変換ルールを記述したjsonファイル')
    parser.add_argument('src', help='入力元ディレクトリ')
    parser.add_argument('dest', help='出力先ディレクトリ')
    parser.add_argument('-r', '--root', action='store_true', help='ルートのファイルも出力する')
    args = parser.parse_args()
    
    process_files(args)

if __name__ == '__main__':
    main()
