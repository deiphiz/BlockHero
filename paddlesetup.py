import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'optimize':2}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Breakout",
        version = "1.0",
        description = "Pong!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("paddlehero.py", base=base)])