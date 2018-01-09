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

'''data_files = []
directories = glob.glob('E:/GitSource/pygame/tetrisResource/image/')
for directory in directories:
    files = glob.glob(directory+'*')
    data_files.append((directory, files))'''

setup(
    name="Metris",
    version="1.0",
    options = options,
    #data_files = data_files,
    #["E:/GitSource/pygame/tetrisResource/image/*", "E:/GitSource/pygame/tetrisResource/audio/*", "E:/GitSource/pygame/tetrisResource/font/*"],
    description = "메트리스(메트로+테트리스) 게임 입니다.",
    author="JayJi(지찬규)",
    author_email = "ckj9014@gmail.com",
    executables = [Executable("playgame.py", base="Win32GUI", icon="icon.ico")])
