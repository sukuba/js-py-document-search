call python2.bat > NUL
cd/D "%WINPYWORKDIR%"
python pdf-to-text.py --normalize %*
