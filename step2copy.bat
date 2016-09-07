rem ################################
rem step2: データをコピーする
rem ################################

@echo %ORIGINAL% から %PUBLISH%\pub\db にコピーします。

robocopy "%ORIGINAL%" %PUBLISH%\pub\db /mir

rem # step2終了. ###
