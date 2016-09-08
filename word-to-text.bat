call python3.bat > NUL
cd/D "%WINPYWORKDIR%"
python word-to-text.py --normalize %*
