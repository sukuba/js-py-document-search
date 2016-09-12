#!/usr/bin/env python

"""
Extracts entire text from Ichitaro document as utf-8 text file.
Works only on Windows with Justsystem Ichitaro installed.
Uses pywin32 to manipulate the Word application.
Expects Python 3

https://github.com/sukuba/js-py-document-search
"""

import argparse
import os.path
import codecs
import win32com.client
import pythoncom

class IchitaroApp(object):
    """
    JXW.Application as a context
    """
    def __init__(self, visible=True, coinitialize=False):
        self.visible = visible
        self.coinitialize = coinitialize
        self.app = None
        
    def __enter__(self):
        if self.coinitialize:
            pythoncom.CoInitialize()
        self.app = win32com.client.DispatchEx('JXW.Application')
        self.app.Application.Visible = self.visible
        return self.app
        
    def __exit__(self, type, value, traceback):
        self.app.Quit
        del self.app
        if self.coinitialize:
            pythoncom.CoUninitialize()
    
class IchitaroDocument(object):
    """
    JXW.Application.Document as a context
    """
    def __init__(self, app, filename):
        self.app = app
        self.filename = filename
        self.doc = None
        
    def __enter__(self):
        print('Opening %s ...' % self.filename)
        self.app.Documents.Open(self.filename)
        """
        Documents.Open doesn't return the Document.
        so this function always return None.
        And,
        The above gives an automation error, 
        so it doesn't work!
        While in the other com server (VBA) can do it as same manner.
        I gave up to dig this any more, 
        because actually I do not own the Ichitaro application.
        """
        return self.doc
        
    def __exit__(self, type, value, traceback):
        self.app.TaroLibrary.QuitDocumentWindow
        print('%s closed.' % self.filename)
    
def get_entire_text(doc, app):
    """
    returns a text of whole document.
    """
    app.TaroLibrary.SelectAll(1)
    # select all text in the windows #1
    texts = app.TaroLibrary.GetString()
    # get selected text lines as a list
    return '\n'.join(texts)
    
def normal_text(text):
    """
    unicode normalization
    """
    import jsngram.text2
    return jsngram.text2.normal_text(text)
    
def ichitaro_to_text(args):
    """
    converts Word document into text files.
    expected args; filename, dest, normalize, invisible, verbose
    """
    with IchitaroApp(visible=not args.invisible) as app:
        with IchitaroDocument(app, args.filename) as doc:
            text = get_entire_text(doc, app)
    if args.normalize:
        text = normal_text(text)
    dest_filename = os.path.join(args.dest, os.path.basename(args.filename) + '.txt')
    with codecs.open(dest_filename, 'w', 'utf-8') as outfile:
        outfile.write(text)
    
    if args.verbose:
        print(args)
        print(dest_filename)
    

def main():
    r"""
    一太郎文書をutf-8 textファイルに変換する。
    
    ichitaro_to_text.py E:\scratch\Hello.jtd E:\scratch
    ichitaro_to_text.py Hello.jtd E:\scratch --normalize
    
    第1引数: 変換元一太郎文書（フルパスまたは出力先パス）
    第2引数: 出力先ディレクトリ（フルパス）
    --normalize: テキストをUnicode正規化する
    --invisible: 一太郎を非表示にする
    --verbose: 冗長な情報を出力する
    
    utf-8 text ファイルを生成する。
    ファイル名は末尾に .txt を付加する。 MyDoc.jtd -> MyDoc.jtd.txt
    Unicode正規化には、jsngram packageを使用する。
    
    一太郎本体が必要（インストール済みであること）。
    
    このプログラムは一太郎を起動し、
    指定された文書ファイルを開き、
    変換したtextを保存し、
    一太郎を閉じる。
    
    """
    parser = argparse.ArgumentParser(description='一太郎文書をutf-8 textファイルに変換する')
    parser.add_argument('filename', help='一太郎文書ファイル名(読み取り)')
    parser.add_argument('dest', help='出力先ディレクトリ')
    parser.add_argument('-n', '--normalize', action='store_true', help='テキストをUnicode正規化する')
    parser.add_argument('-i', '--invisible', action='store_true', help='一太郎を非表示にする')
    parser.add_argument('-v', '--verbose', action='store_true', help='冗長な情報を出力する')
    args = parser.parse_args()
    
    args.filename = os.path.join(args.dest, args.filename)
    
    if args.verbose:
        print(args)
    ichitaro_to_text(args)

if __name__ == '__main__':
    main()
