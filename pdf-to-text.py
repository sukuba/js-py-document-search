#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 2 with python 3 flavor using utf-8
# pdfminer is for python 2
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Extracts entire text from pdf file as utf-8 text file.
Requires pdfminer.
Expects Python 2

https://github.com/sukuba/js-py-document-search
"""

import argparse
import os.path
import codecs

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

def normal_text(file):
    """
    unicode normalization
    """
    import jsngram.text2
    return jsngram.text2.normalize_texts(file)
    
def pdf_to_text(args):
    """
    converts PDF file into text files.
    expected args; filename, dest, normalize
    many parts of this function comes from pdf2txt.py distributed with pdfminer.
    """
    outfile = os.path.join(args.dest.decode('cp932'), os.path.basename(args.filename.decode('cp932')) + '.txt')
    outtype = 'text'
    codec = 'utf-8'
    
    password = ''
    pagenos = set()
    maxpages = 0
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    
    debug = 0
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    
    rsrcmgr = PDFResourceManager(caching=caching)
    outfp = file(outfile, 'w')
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                           imagewriter=imagewriter)
    fp = file(args.filename, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.close()
    
    if args.normalize:
        text = normal_text(outfile)
    
    if args.verbose:
        print(args)
        print(outfile)
    

def main():
    r"""
    ＰＤＦファイルをutf-8 textファイルに変換する。
    
    pdf-to-text.py E:\scratch\Hello.pdf E:\scratch
    pdf-to-text.py Hello.pdf E:\scratch --normalize
    
    第1引数: 変換元ＰＤＦ文書（フルパスまたは出力先パス）
    第2引数: 出力先ディレクトリ（フルパス）
    --normalize: テキストをUnicode正規化する
    --verbose: 冗長な情報を出力する
    
    utf-8 text ファイルを生成する。
    ファイル名は末尾に .txt を付加する。 MyPdf.pdfc -> MyPdf.pdf.txt
    Unicode正規化には、jsngram packageを使用する。
    
    pdfminer が必要。
    
    """
    parser = argparse.ArgumentParser(description='ＰＤＦファイルをutf-8 textファイルに変換する')
    parser.add_argument('filename', help='ＰＤＦファイル名(読み取り)')
    parser.add_argument('dest', help='出力先ディレクトリ')
    parser.add_argument('-n', '--normalize', action='store_true', help='テキストをUnicode正規化する')
    parser.add_argument('-v', '--verbose', action='store_true', help='冗長な情報を出力する')
    args = parser.parse_args()
    
    args.filename = os.path.join(args.dest, args.filename)
    
    if args.verbose:
        print(args)
    pdf_to_text(args)

if __name__ == '__main__':
    main()
