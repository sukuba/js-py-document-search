rem ################################
rem step2: データをコピーする
rem ################################

if "%ORIGINAL%" == "" goto TERMINATE
if "%PUBLISH%" == "" goto TERMINATE

@echo %ORIGINAL% から %PUBLISH%\pub\db にコピーします。

robocopy "%ORIGINAL%" %PUBLISH%\pub\db /mir /xa:SHT

rem # step2終了. ###
exit /B

:TERMINATE
pause エラー: step1が正しく動いていないので、中止します。
exit 1
