import sys, os
from pathlib import Path

# Things related to paths for the app
# class method to return the current Profile Path
def ProfilePath(config): return Path(config.Read('ProfilePath'))

# This relies on this file, Paths.py, staying exactly one level down, in /Util
def GetRootDirPath():
    base_path = getattr(sys, '_MEIPASS', '')
    if base_path:
        base_path = Path(base_path)
    else:
        base_path = Path(os.path.abspath(__file__)).parent.parent

    return base_path

