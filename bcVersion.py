import platform
import os
import shutil
import subprocess
from Util.Paths import GetRootDirPath

def current_version():
    # try to get the current tag from git...
    version = get_git_tag()

    # if not, try to find version.txt
    #
    # version.txt gets written/bundled by tools/build_windows.bat
    if not version:
        try:
            base_path = GetRootDirPath()
            file_path = base_path / "version.txt"
            version = file_path.read_text().strip()
        except:
            pass

    if not version:
        version = "&lt; No version found &gt;"

    return version

def get_git_tag(path=None):
    if not path: path = os.path.curdir

    tag = None

    # we'll try asl git, mostly just for me.  If that breaks, try just plain git
    command = 'git describe --tags'
    if wsl_available():
        try:    tag = do_git("wsl " + command, path)
        except: pass

    if not tag:
        try:    tag = do_git(command, path)
        except: pass

    return tag

def do_git(command, path):
    tag = None
    proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE, cwd=path)
    out  = proc.stdout
    if out :
        tag = out.read().decode('utf-8')
    if tag:
        return tag.strip()

### two functions below from https://github.com/scivision/detect-windows-subsystem-for-linux
#
# Copyright (c) 2023 scivision
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
def is_wsl(v: str = platform.uname().release) -> int:
    ### detects if Python is running in WSL

    if v.endswith("-Microsoft"):
        return 1
    elif v.endswith("microsoft-standard-WSL2"):
        return 2

    return 0


def wsl_available() -> int:
    ### detect if Windows Subsystem for Linux is available from Windows

    if os.name != "nt" or not shutil.which("wsl"):
        return False
    try:
        return is_wsl(
            subprocess.check_output(
                ["wsl", "uname", "-r"], text=True, timeout=15
            ).strip()
        )
    except subprocess.SubprocessError:
        return False


