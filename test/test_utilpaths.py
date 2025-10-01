import wx
import sys
from pathlib import Path
import pytest
from Util.Paths import ProfilePath, GetRootDirPath, CheckProfileForBindsDir, GetProfileFileForName, GetAllProfileBindsDirs, GetValidGamePath, GetPopmenuPath

def test_CheckProfileForBindsDir(config, tmp_path):
    # CheckProfileForBindsDir
    pdir = tmp_path / 'fubble'
    pdir.mkdir(exist_ok = True)
    file = pdir / 'bcprofileid.txt'
    file.write_text('Mister Fubble')
    assert CheckProfileForBindsDir(config, 'fubble') == 'Mister Fubble'
    file.unlink()
    pdir.rmdir()

def test_GetProfileFileForName(config, tmp_path):
    # GetProfileFileForName
    file = tmp_path / 'fubble.bcp'
    file.write_text('freebird')
    assert str(GetProfileFileForName(config, 'fubble')) == f'{tmp_path}/fubble.bcp'
    file.unlink()

def test_GetAllProfileBindsDirs(config, tmp_path):
    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.mkdir(exist_ok = True)

    assert sorted(GetAllProfileBindsDirs(config)) == sorted(['inky', 'pinky', 'blinky', 'clyde'])

    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.rmdir()

def test_ProfilePath(config, tmp_path):
    assert ProfilePath(config) == tmp_path

def test_GetRootDirPath(monkeypatch, tmp_path):
    assert GetRootDirPath() == Path(__file__).resolve().parent.parent
    monkeypatch.setattr(sys, '_MEIPASS', tmp_path, raising = False)
    assert GetRootDirPath() == Path(tmp_path)
    monkeypatch.undo()

def test_GetValidGamePath(config, tmp_path):
    config.Write('GamePath', str(tmp_path))
    assert not GetValidGamePath('Homecoming')
    assert not GetValidGamePath('Rebirth')

    Path(tmp_path / 'bin').mkdir()
    Path(tmp_path / 'assets').mkdir()
    assert GetValidGamePath('Homecoming') == tmp_path
    Path(tmp_path / 'bin').rmdir()
    Path(tmp_path / 'assets').rmdir()

    config.Write('GameRebirthPath', str(tmp_path))
    Path(tmp_path / 'Rebirth.exe').touch()
    assert GetValidGamePath('Rebirth') == tmp_path
    Path(tmp_path / 'Rebirth.exe').unlink()

    with pytest.raises(Exception, match = 'GetValidGamePath got an unknown'):
        GetValidGamePath('No Such Server')

def test_GetPopmenuPath(config, monkeypatch, tmp_path):
    monkeypatch.undo() # get rid of config.Read patch
    config.Write('GamePath', str(tmp_path))
    config.Write('GameLang', 'en')
    Path(tmp_path / 'bin').mkdir()
    Path(tmp_path / 'assets').mkdir()
    assert GetPopmenuPath('Homecoming') == tmp_path / 'data' / 'Texts' / 'en' / 'Menus'

    Path(tmp_path / 'DAtA').mkdir()
    assert GetPopmenuPath('Homecoming') == tmp_path / 'DAtA' / 'Texts' / 'en' / 'Menus'

    Path(tmp_path / 'bin').rmdir()
    Path(tmp_path / 'assets').rmdir()
    Path(tmp_path / 'DAtA').rmdir()

#########
@pytest.fixture(autouse = True)
def config(tmp_path, monkeypatch):
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    monkeypatch.setattr(config, 'Read', lambda _: str(tmp_path))
    yield config
