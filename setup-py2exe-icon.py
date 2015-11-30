#!/usr/bin/python

# ...
# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
try:
    # py2exe 0.6.4 introduced a replacement modulefinder.
    # This means we have to add package paths there, not to the built-in
    # one.  If this new modulefinder gets integrated into Python, then
    # we might be able to revert this some day.
    # if this doesn't work, try import modulefinder
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com, sys
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass

from distutils.core import setup
import py2exe

import sys, os, site, shutil, stat, time
  
site_dir = site.getsitepackages()[1] 
include_dll_path = os.path.join(site_dir, "gnome") 
  
gtk_dirs_to_include = ['etc', 'lib\\gtk-3.0', 'lib\\girepository-1.0', 'lib\\gio', 'lib\\gdk-pixbuf-2.0', 'share\\glib-2.0', 'share\\fonts', 'share\\icons', 'share\\themes\\Default', 'share\\themes\\HighContrast'] 

include_gi_path = os.path.join(site_dir, "gi")

gtk_dlls = [] 
tmp_dlls = [] 
cdir = os.getcwd() 
for dll in os.listdir(include_dll_path): 
    if dll.lower().endswith('.dll'): 
        gtk_dlls.append(os.path.join(include_dll_path, dll)) 
        tmp_dlls.append(os.path.join(cdir, dll)) 
  
for dll in gtk_dlls: 
    shutil.copy(dll, cdir) 
          
setup(
     windows=[{
     'script':'yadns.py',
     'icon_resources':[(1, "yaicon.ico")],
     }],
     name="yadns",
     version="1.0",
     description="Yet another DNS",
     author="Galen Senogles",
     py_modules=["yadns"],
     options={
      'py2exe': {
      'includes' : 'gi',
      'packages': 'gi',
      'bundle_files': 3,
      'dll_excludes': ["mswsock.dll", "powrprof.dll", "KERNELBASE.dll",
      "API-MS-Win-Core-LocalRegistry-L1-1-0.dll",
      "API-MS-Win-Core-ProcessThreads-L1-1-0.dll",
      "API-MS-Win-Security-Base-L1-1-0.dll",
      "api-ms-win-core-delayload-l1-1-1.dll",
      "api-ms-win-core-errorhandling-l1-1-1.dll",
      "api-ms-win-core-handle-l1-1-0.dll",
      "api-ms-win-core-heap-l1-2-0.dll",
      "api-ms-win-core-heap-obsolete-l1-1-0.dll",
      "api-ms-win-core-libraryloader-l1-2-0.dll",
      "api-ms-win-core-localization-obsolete-l1-2-0.dll",
      "api-ms-win-core-processthreads-l1-1-2.dll",
      "api-ms-win-core-profile-l1-1-0.dll",
      "api-ms-win-core-registry-l1-1-0.dll",
      "api-ms-win-core-string-l1-1-0.dll",
      "api-ms-win-core-string-obsolete-l1-1-0.dll",
      "api-ms-win-core-synch-l1-2-0.dll",
      "api-ms-win-core-sysinfo-l1-2-1.dll",
      "api-ms-win-security-base-l1-2-0.dll",
      "crypt32.dll", "WLDAP32.dll",
      ]
      }
    },
    zipfile=None)

dest_dir = os.path.join(cdir, os.path.abspath("dist"))
print dest_dir
print 'Sleeping five seconds'
time.sleep(5)
print 'Copying files'
for dll in tmp_dlls:
    try:
      shutil.copy(dll, dest_dir)
    except IOError:
      time.sleep(5)
      shutil.copy(dll, dest_dir)
    fileAtt = os.stat(dll)[0]
    os.chmod(dll, stat.S_IWRITE)
    os.remove(dll) 
  
for d  in gtk_dirs_to_include: 
    shutil.copytree(os.path.join(site_dir, "gnome", d), os.path.join(dest_dir, d))