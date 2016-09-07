rem ################################
rem step3: 収録ファイル一覧.xls を読み込む
rem ################################

python excel-to-json.py %PUBLISH%\pub\db %MyTMP% --pattern 収録ファイル一覧.*\.xls --sheet 実施課題一覧 --columns A:F --url E --formula

python make-fileinfo.py %MyTMP%\sheet1.json %PUBLISH%\pub\fileinfo.json --key 6 --value 4 5 1 2 3 0 --convertbackslash

rem # step3終了. ###
