import sys
from pathlib import Path
import pytest
import Util.Paths
from Util.Paths import ProfilePath, GetRootDirPath, CheckProfileForBindsDir, GetProfileFileForName, GetAllProfileBindsDirs, GetValidGamePath, GetPopmenuPath

def test_CheckProfileForBindsDir(config, monkeypatch, tmp_path):
    config.WriteBool('RelativeBindsDir', False)

    # Absolute path
    pdir = tmp_path / 'fubble'
    pdir.mkdir(exist_ok = True, parents = True)
    file = pdir / 'bcprofileid.txt'
    file.write_text('Mister Fubble')
    assert CheckProfileForBindsDir(config, 'fubble') == 'Mister Fubble'
    file.unlink()
    pdir.rmdir()

    # Relative paths
    config.WriteBool('RelativeBindsDir', True)
    monkeypatch.setattr(Util.Paths, 'GetValidGamePath', lambda _,__: tmp_path)
    # no server == Homecoming
    pdir = tmp_path / 'settings' / 'live' / 'mumble'
    pdir.mkdir(exist_ok = True, parents = True)
    file = pdir / 'bcprofileid.txt'
    file.write_text('Peg')
    assert CheckProfileForBindsDir(config, 'mumble') == 'Peg'
    file.unlink()
    pdir.rmdir()
    # Rebirth
    pdir = tmp_path / 'piggs' / 'wordjazz'
    pdir.mkdir(exist_ok = True, parents = True)
    file = pdir / 'bcprofileid.txt'
    file.write_text('stare')
    assert CheckProfileForBindsDir(config, 'wordjazz', 'Rebirth') == 'stare'
    file.unlink()
    pdir.rmdir()

def test_GetProfileFileForName(config, tmp_path):
    file = tmp_path / 'fubble.bcp'
    file.write_text('freebird')
    assert str(GetProfileFileForName(config, 'fubble')) == f'{tmp_path}/fubble.bcp'
    file.unlink()

def test_GetAllProfileBindsDirs(config, monkeypatch, tmp_path):
    # absolute path
    profiledirs = ['inky', 'pinky', 'blinky', 'clyde']
    for d in profiledirs:
        pdir = tmp_path / d
        pdir.mkdir(exist_ok = True)

    assert sorted(GetAllProfileBindsDirs(config)) == sorted(profiledirs)

    for d in profiledirs:
        pdir = tmp_path / d
        pdir.rmdir()

    # relative paths
    config.WriteBool('RelativeBindsDir', True)
    monkeypatch.setattr(Util.Paths, 'GetValidGamePath', lambda _,__: tmp_path)
    # Homecoming
    for d in profiledirs:
        pdir = tmp_path / 'settings'/ 'live' / d
        pdir.mkdir(exist_ok = True, parents = True)

    assert sorted(GetAllProfileBindsDirs(config)) == sorted(profiledirs)

    for d in profiledirs:
        pdir = tmp_path / 'settings' / 'live' / d
        pdir.rmdir()

    # Homecoming
    for d in profiledirs:
        pdir = tmp_path / 'piggs' / d
        pdir.mkdir(exist_ok = True, parents = True)

    assert sorted(GetAllProfileBindsDirs(config, 'Rebirth')) == sorted(profiledirs)

    for d in profiledirs:
        pdir = tmp_path / 'piggs' / d
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
    assert not GetValidGamePath(config, 'Homecoming')
    assert not GetValidGamePath(config, 'Rebirth')

    Path(tmp_path / 'bin').mkdir()
    Path(tmp_path / 'assets').mkdir()
    assert GetValidGamePath(config, 'Homecoming') == tmp_path
    Path(tmp_path / 'bin').rmdir()
    Path(tmp_path / 'assets').rmdir()

    config.Write('GameRebirthPath', str(tmp_path))
    Path(tmp_path / 'Rebirth.exe').touch()
    assert GetValidGamePath(config, 'Rebirth') == tmp_path
    Path(tmp_path / 'Rebirth.exe').unlink()

    with pytest.raises(Exception, match = 'GetValidGamePath got an unknown'):
        GetValidGamePath(config, 'No Such Server')

def test_GetPopmenuPath(config, monkeypatch, tmp_path):
    monkeypatch.undo() # get rid of config.Read patch
    config.Write('GamePath', str(tmp_path))
    config.Write('GameLang', 'en')
    Path(tmp_path / 'bin').mkdir()
    Path(tmp_path / 'assets').mkdir()
    assert GetPopmenuPath(config, 'Homecoming') == tmp_path / 'data' / 'Texts' / 'en' / 'Menus'

    Path(tmp_path / 'DAtA').mkdir()
    assert GetPopmenuPath(config, 'Homecoming') == tmp_path / 'DAtA' / 'Texts' / 'en' / 'Menus'

    Path(tmp_path / 'bin').rmdir()
    Path(tmp_path / 'assets').rmdir()
    Path(tmp_path / 'DAtA').rmdir()
