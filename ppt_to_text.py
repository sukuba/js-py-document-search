#!/usr/bin/env python

"""
Extracts entire text from Power Point presentation as utf-8 text file.
Works only on Windows with Ms Power Point installed.
Uses pywin32 to manipulate the Power Point application.
Expects Python 3

https://github.com/sukuba/js-py-document-search
"""

import argparse
import os
import shutil
import codecs
import win32com.client
import pythoncom

class PowerPointApp(object):
    """
    PowerPoint.Application as a context
    """
    def __init__(self, visible=True, coinitialize=False):
        self.visible = visible
        self.coinitialize = coinitialize
        self.app = None
        
    def __enter__(self):
        if self.coinitialize:
            pythoncom.CoInitialize()
        self.app = win32com.client.DispatchEx('PowerPoint.Application')
        self.app.Visible = self.visible
        self.app.DisplayAlerts = 1  # ppAlertsNone
        return self.app
        
    def __exit__(self, type, value, traceback):
        self.app.Quit()
        del self.app
        if self.coinitialize:
            pythoncom.CoUninitialize()
    
class PowerPointPresentation(object):
    """
    PowerPoint.Application.Presentation as a context
    """
    def __init__(self, app, filename):
        self.app = app
        self.filename = filename
        self.doc = None
        
    def __enter__(self):
        print('Opening %s ...' % self.filename)
        self.doc = self.app.Presentations.Open(self.filename, -1)  # ReadOnly
        return self.doc
        
    def __exit__(self, type, value, traceback):
        self.doc.Saved = -1  # set as saved
        self.doc.Close()
        del self.doc
        print('%s closed.' % self.filename)
    
def save_as_rtf(presentation, filename):
    presentation.SaveCopyAs(filename, 6, 0)  # as RTF, no embed font
    
def get_temporary_name(filename, tempdir):
    # use same name as src file at tempdir.
    destname = os.path.join(tempdir, os.path.basename(filename) + '.rtf')
    return destname

def ppt_to_text(args):
    """
    converts Power Point presentation into text files.
    converts ppt to rtf, and then use word-to-text converter inside.
    expected args; filename, dest, tempdir, keeptemp, normalize, invisible, verbose
    """
    temp_doc = get_temporary_name(args.filename, args.tempdir)
    
    with PowerPointApp(visible=not args.invisible) as app:
        with PowerPointPresentation(app, args.filename) as doc:
            save_as_rtf(doc, temp_doc)
    
    fake_name = temp_doc[:-4]  # remove the last '.rtf'
    if os.path.exists(fake_name):
        print('CAUTION!!  OVERWRITE FILE: %s' % fake_name)
    shutil.copyfile(temp_doc, fake_name)  # rename is danger on Windows
    # if tempdir is same as source dir, this will overwirte the source file!!
    
    import word_to_text
    args.filename = fake_name
    word_to_text.word_to_text(args)
    
    if not args.keeptemp:
        os.remove(temp_doc)
        os.remove(fake_name)

def main():
    r"""
    パワーポイント文書をutf-8 textファイルに変換する。
    
    ppt_to_text.py E:\scratch\Hello.doc E:\scratch E:\tmp
    ppt_to_text.py Hello.doc E:\scratch E:\tmp --normalize
    
    第1引数: 変換元パワーポイント文書（フルパスまたは出力先パス）
    第2引数: 出力先ディレクトリ（フルパス）
    --tempdir: 一時ファイル作業用ディレクトリ（フルパス）
    --keeptemp: 一時ファイルを削除しない
    --normalize: テキストをUnicode正規化する
    --invisible: ワードを非表示にする
    --verbose: 冗長な情報を出力する
    
    utf-8 text ファイルを生成する。
    ファイル名は末尾に .txt を付加する。 MyPpt.ppt -> MyPpt.ppt.txt
    Unicode正規化には、jsngram packageを使用する。
    
    パワーポイントとワード本体が必要（インストール済みであること）。
    
    一時ファイル作業用ディレクトリには、
    必ず、必要なファイルが無いディレクトリを指定する。
    ここにあるファイルは無条件に上書き変更する。
    
    このプログラムはパワーポイントを起動し、
    指定された文書ファイルを開き、
    rtfとして一時ディレクトリに保存し、
    パワーポイントを閉じる。
    さらに word_to_text.py を利用して、
    rtfを開き、
    変換したtextを保存する。
    
    """
    parser = argparse.ArgumentParser(description='パワーポイント文書をutf-8 textファイルに変換する')
    parser.add_argument('filename', help='パワーポイント文書ファイル名(読み取り)')
    parser.add_argument('dest', help='出力先ディレクトリ')
    parser.add_argument('-t', '--tempdir', type=str, help='一時ファイル作業用ディレクトリ')
    parser.add_argument('-k', '--keeptemp', action='store_true', help='一時ファイルを削除しない')
    parser.add_argument('-n', '--normalize', action='store_true', help='テキストをUnicode正規化する')
    parser.add_argument('-i', '--invisible', action='store_true', help='ワードを非表示にする')
    parser.add_argument('-v', '--verbose', action='store_true', help='冗長な情報を出力する')
    args = parser.parse_args()
    
    args.filename = os.path.join(args.dest, args.filename)
    
    if args.verbose:
        print(args)
    ppt_to_text(args)

if __name__ == '__main__':
    main()
