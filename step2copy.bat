rem ################################
rem step2: �f�[�^���R�s�[����
rem ################################

if "%ORIGINAL%" == "" goto TERMINATE
if "%PUBLISH%" == "" goto TERMINATE

@echo %ORIGINAL% ���� %PUBLISH%\pub\db �ɃR�s�[���܂��B

robocopy "%ORIGINAL%" %PUBLISH%\pub\db /mir /xa:SHT

rem # step2�I��. ###
exit /B

:TERMINATE
pause �G���[: step1�������������Ă��Ȃ��̂ŁA���~���܂��B
exit 1
