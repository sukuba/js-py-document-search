#!/usr/bin/env python

"""
Normalize unicode (utf-8) text file.
Expects Python 3

https://github.com/sukuba/js-py-document-search
"""

import argparse
import os.path
import codecs

def normal_text(text):
    """
    unicode normalization
    """
    import jsngram.text2
    jsngram.text2.normalize_texts(file)
    
def normalize_text(args):
    """
    Normalize unicode (utf-8) text file.
    expected args; filename
    """
    normal_text(text)
    

def main():
    r"""
    utf-8 textファイルをUnicode正規化する。
    
    normalize-text.py E:\scratch\Hello.txt
    
    第1引数: 対象ファイル（フルパス、上書き変更）
    
    指定されたutf-8テキストファイルを読み込み、
    Unicode正規化した結果を、
    同じファイルにutf-8で上書きする。
    
    """
    parser = argparse.ArgumentParser(description='utf-8 textファイルをUnicode正規化する')
    parser.add_argument('filename', help='対象ファイル（フルパス、上書き変更）')
    args = parser.parse_args()
    
    normalize_text(args)

if __name__ == '__main__':
    main()
