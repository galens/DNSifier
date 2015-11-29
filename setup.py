﻿import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
#build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
build_exe_options = {}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "yadns",
        version = "0.1",
        description = "A small local DNS",
        options = {"build_exe": build_exe_options},
        executables = [Executable("yadns.py", base=base)])