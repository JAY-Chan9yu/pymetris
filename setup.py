import sys
from cx_Freeze import setup, Executable
import glob
base = None

packages = ["time","tetris","blocklib","random","math", "pygame"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name="Metris",
    version="1.0",
    options = options,
    author="JayJi(지찬규)",
    author_email = "ckj9014@gmail.com",
    executables = [Executable("playgame.py", base="Win32GUI", icon="icon.ico")])
