from pathlib import Path, PureWindowsPath
import BindFile

def test_accessors(config, profile, tmp_path):
    config.Write('BindPath', str(tmp_path))
    assert profile.ProfileName()     == 'testprofile'
    assert profile.Archetype()       == 'Arachnos Soldier'
    assert profile.Primary()         == 'Crab Spider Soldier'
    assert profile.Secondary()       == 'Crab Spider Training'
    assert profile.Server()          == 'Rebirth'
    assert profile.Filepath()        == Path(__file__).resolve().parent / 'fixtures' / 'testprofile.bcp'
    assert profile.ProfileBindsDir() == 'testprofile'
    assert profile.BindsDir()        == Path(tmp_path / profile.ProfileBindsDir())
    assert profile.GameBindsDir()    == PureWindowsPath('c:/coh/testprofile')
    # TODO put GameBindPath into Config and try again
    config.Write('GameBindPath', str(tmp_path))
    assert profile.GameBindsDir()    == PureWindowsPath(tmp_path / profile.ProfileBindsDir())

    assert profile.HasPowerPool('Flight')
    assert profile.HasPowerPool('Gadgetry')
    assert profile.HasPowerPool('Presence')
    assert profile.HasPowerPool('Leadership')

    assert profile.HasPower('Flight', 'Hover') # checks the "nothing specified" path
    assert profile.GetCustomID() == 11

def test_BLF(profile):
    assert profile.BLF('test') == '$$bindloadfilesilent c:\\coh\\testprofile\\test'
    assert profile.BLF('test', 'more', 'chunks') == '$$bindloadfilesilent c:\\coh\\testprofile\\test\\more\\chunks'

def test_GetBindFile(config, profile):
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
