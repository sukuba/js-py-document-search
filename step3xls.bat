rem ################################
rem step3: ���^�t�@�C���ꗗ.xls ��ǂݍ���
rem ################################

python excel-to-json.py %PUBLISH%\pub\db %MyTMP% --pattern ���^�t�@�C���ꗗ.*\.xls --sheet ���{�ۑ�ꗗ --columns A:F --url E --formula

python make-fileinfo.py %MyTMP%\sheet1.json %PUBLISH%\pub\fileinfo.json --key 6 --value 4 5 1 2 3 0 --convertbackslash

rem # step3�I��. ###
