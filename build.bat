rem c:\Python27\python.exe dnschef.py --fakeip=127.0.0.1 --fakedomains=google.com --nameservers=172.26.104.21
rem c:\Python34\python.exe c:\Python34\Scripts\cxfreeze yadns.py --target-dir dist
rem c:\Python34\python.exe setup-py2exe.py py2exe
rem c:\Python27\python.exe setup-py2exe.py py2exe
rem c:\Python27\python.exe setup-py2exe-icon.py py2exe
c:\Python27\Scripts\pyinstaller.exe --icon yaicon.ico --noconsole yadns.py
