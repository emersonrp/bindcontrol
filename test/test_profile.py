from pathlib import Path, PureWindowsPath
import platform
import BindFile
import Util.Paths

def test_accessors(config, monkeypatch, profile, tmp_path):
    config.Write('BindPath', str(tmp_path))
    config.Write('GameRebirthPath', str(tmp_path))
    monkeypatch.setattr(Util.Paths, 'GetValidGamePath', lambda _: tmp_path)
    assert profile.ProfileName()     == 'testprofile'
    assert profile.Archetype()       == 'Arachnos Soldier'
    assert profile.Primary()         == 'Crab Spider Soldier'
    assert profile.Secondary()       == 'Crab Spider Training'
    assert profile.Server()          == 'Rebirth'
    assert profile.Filepath()        == Path(__file__).resolve().parent / 'fixtures' / 'testprofile.bcp'
    assert profile.ProfileBindsDir() == 'testprofile'
    assert profile.BindsDir()        == Path('kb') / profile.ProfileBindsDir()
    assert profile.BindsPath()       == tmp_path / 'piggs' / profile.BindsDir() # this is a little hard-coded ugly
    assert profile.GameBindsDir()    == Path('kb/testprofile')

    config.WriteBool('RelativeBindsDir', False)
    assert profile.BindsDir()        == Path(tmp_path / profile.ProfileBindsDir())
    assert profile.BindsPath()       == profile.BindsDir()
    assert profile.GameBindsDir()    == PureWindowsPath('c:/coh/testprofile')

    config.Write('GameBindPath', str(tmp_path))
    assert profile.GameBindsDir()    == PureWindowsPath(tmp_path / profile.ProfileBindsDir())

    assert profile.HasPowerPool('Flight')
    assert profile.HasPowerPool('Gadgetry')
    assert profile.HasPowerPool('Presence')
    assert profile.HasPowerPool('Leadership')

    assert profile.HasPower('Flight', 'Hover') # checks the "nothing specified" path
    assert profile.GetCustomID() == 11

def test_BLF(config, profile):
    sep = '\\' if platform.system() == 'Windows' else '/'
    assert profile.BLF('test') == f'$$bindloadfilesilent kb{sep}testprofile{sep}test'
    assert profile.BLF('test', 'more', 'chunks') == f'$$bindloadfilesilent kb{sep}testprofile{sep}test{sep}more{sep}chunks'
    config.WriteBool('RelativeBindsDir', False)
    assert profile.BLF('test') == '$$bindloadfilesilent c:\\coh\\testprofile\\test'
    assert profile.BLF('test', 'more', 'chunks') == '$$bindloadfilesilent c:\\coh\\testprofile\\test\\more\\chunks'

def test_GetBindFile(config, profile):
    config.WriteBool('RelativeBindsDir', False)
    assert 'test_bindfile.txt' not in profile.BindFiles
    bindfile = profile.GetBindFile('test_bindfile.txt')
    assert isinstance(bindfile, BindFile.BindFile)
    assert bindfile.Path == Path(profile.BindsDir() / 'test_bindfile.txt')
    assert 'test_bindfile.txt' in profile.BindFiles

    assert 'fubble/moretest.txt' not in profile.BindFiles
    bindfile = profile.GetBindFile('fubble', 'moretest.txt')
    assert isinstance(bindfile, BindFile.BindFile)
    assert bindfile.Path == Path(profile.BindsDir() / 'fubble' / 'moretest.txt')
    assert 'fubble/moretest.txt' in profile.BindFiles
