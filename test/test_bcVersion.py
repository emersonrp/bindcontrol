#!/usr/sbin/python
import os
import shutil
import subprocess
import bcVersion
import Util.Paths

def test_version_txt(monkeypatch, tmp_path):
    monkeypatch.setattr(Util.Paths, 'GetRootDirPath', lambda: tmp_path)
    version_txt = tmp_path / 'version.txt'
    version_txt.write_text('test_version_1.1.1\n')
    assert bcVersion.current_version() == 'test_version_1.1.1'
    monkeypatch.undo()

def test_get_git_tag(monkeypatch):
    assert bcVersion.get_git_tag() != ''
    assert bcVersion.current_version() is not None
    monkeypatch.setattr(bcVersion, 'get_git_tag', lambda: None)
    assert bcVersion.current_version() == "&lt; No version found &gt;"
    monkeypatch.undo()

def test_is_wsl():
    assert bcVersion.is_wsl('not WSL thanks') == 0
    assert bcVersion.is_wsl('fubble-Microsoft') == 1
    assert bcVersion.is_wsl('wubble-microsoft-standard-WSL2') == 2

def test_wsl_coverage(monkeypatch):
    monkeypatch.setattr(bcVersion, 'wsl_available', lambda: True)
    assert bcVersion.get_git_tag() != ''
    monkeypatch.undo()

    monkeypatch.setattr(bcVersion, 'do_git', lambda _,__: 1/0) # raises exception
    assert bcVersion.get_git_tag() == ''

    monkeypatch.setattr(os, 'name', 'nt')
    monkeypatch.setattr(shutil, 'which', lambda _: True)
    monkeypatch.setattr(subprocess, 'check_output', raise_subprocess_exception)
    assert bcVersion.wsl_available() is False


def raise_subprocess_exception(*_, **__):
    raise(subprocess.SubprocessError)
