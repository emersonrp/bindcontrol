import subprocess
import os
import sys

def get_git_tag(path=None):
    if path is None:
        path = os.path.curdir
    command = 'git describe --tags'.split()
    try:
        tag = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path).stdout.read().decode('utf-8')
        return tag.strip()
    except:
        return None

def current_version():
    version = get_git_tag()

    if not version:
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            filename = f"{base_path}/version.txt"
            with open(filename, 'r') as file:
                version = file.read().strip()
        except:
            pass

    if not version:
        version = "No version found"

    return version
