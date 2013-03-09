import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'icon':'icon.ico', 'optimize':2}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Block Hero & Paddle Hero!",
        version = "1.1",
        description = "A simple Breakout and Pong clone",
        options = {"build_exe": build_exe_options},
        executables = [Executable("blockhero.py", base=base)])