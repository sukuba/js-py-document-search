set WINPYDIR=C:\sukuba\bin\WinPython3\python-3.4.4.amd64
set WINPYVER=3.4.4.3Qt5
set HOME=%WINPYDIR%\..\settings
set WINPYARCH="WIN32"
if  "%WINPYDIR:~-5%"=="amd64" set WINPYARCH="WIN-AMD64"

set PATH=%WINPYDIR%\Lib\site-packages\PyQt5;%WINPYDIR%\Lib\site-packages\PyQt4;%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%WINPYDIR%\..\tools;%WINPYDIR%\..\tools\mingw32\bin;%PATH%;

rem force default pyqt5 kit for Spyder if PyQt5 module is there
if exist %WINPYDIR%\Lib\site-packages\PyQt5 set QT_API=pyqt5

set WINPYWORKDIR=C:\sukuba\tmp
rem cd/D "%WINPYWORKDIR%"
