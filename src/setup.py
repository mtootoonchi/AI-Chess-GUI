import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["AIchess", "main", "tkinter", "random"], "include_files": []}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "AI-Chess",
        version = "2.0.0",
        description = "AI Chess Windows executable",
        options = {"AI-Chess_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])