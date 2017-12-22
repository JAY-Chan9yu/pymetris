import sys
from cx_Freeze import setup, Executable

base = None

build_exe_options = dict(
        compressed = True,
        includes = ["time","tetris","blocklib","random","math", "pygame"],
        include_files = []
)
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
    description = "실행 파일로 배포",
    author="JAYJI",
    executables = [Executable("playgame.py", base="Win32GUI")])
