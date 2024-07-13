#!/usr/sbin/python
import subprocess

import bcVersion

def git_found():
    try:
        subprocess.call(['git', '--version'], stdout=subprocess.DEVNULL)
        return True
    except:
        return False

def test_get_git_tag():
    if git_found():
        assert bcVersion.get_git_tag() is not None
    else:
        assert bcVersion.get_git_tag() is None

