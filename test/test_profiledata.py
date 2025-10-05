#!/usr/sbin/python
import wx
import os
import platform
import pytest
import json
import Models.ProfileData as ProfileData
from time import sleep
from pathlib import Path, PureWindowsPath
from BindFile import BindFile
from Util.BuildFiles import ParseBuildFile
import Util.Paths

def test_init_empty():
    with pytest.raises(Exception, match = 'neither filename nor newname'):
        ProfileData.ProfileData(config)

def test_init_newname(config, monkeypatch):
    monkeypatch.undo()
    PD = ProfileData.ProfileData(config, newname = 'test')
    assert PD.Config             == config
    assert PD.Filepath           == Util.Paths.ProfilePath(config) / 'test.bcp'
    assert PD['ProfileBindsDir'] == 'test'
    assert PD.IsModified()

    monkeypatch.setattr(ProfileData.ProfileData, 'GenerateBindsDirectoryName', lambda _: '')
    with pytest.raises(Exception, match = 'sane Binds Directory'):
        ProfileData.ProfileData(config, newname = 'nobindsdir')
    monkeypatch.undo()

    assert PD.IsModified()

def test_defaultprofile(config, DefaultProfile, monkeypatch):
    monkeypatch.undo() # get rid of "Read" monkeypatch on config
    config.Write('DefaultProfile', DefaultProfile)
    # newname == use Default Profile
    PD = ProfileData.ProfileData(config, newname = 'test')
    assert PD['General']['Archetype'] == 'Blaster'
    assert PD['General']['Origin'] == 'Magic'
    assert PD['General']['Server'] == 'Homecoming'
    assert PD['General']['Primary'] == 'Archery'
    assert PD['General']['Secondary'] == 'Atomic Manipulation'

    assert PD.IsModified()

    monkeypatch.setattr(json, 'loads', raises_exception)
    with pytest.raises(Exception, match = 'while loading Default Profile'):
        ProfileData.ProfileData(config, newname = 'explode')

def test_init_buildfile(config, DefaultProfile, monkeypatch):
    monkeypatch.undo()
    buildfile = Path(__file__).resolve().parent / 'fixtures' / 'buildfile.txt'
    profiledata = { 'General' : ParseBuildFile(buildfile) }
    config.Write('DefaultProfile', DefaultProfile)
    PD = ProfileData.ProfileData(config, newname = 'fubble', profiledata = profiledata)
    assert PD['General']['Name'] == 'Fixture'
    assert PD['General']['Archetype'] == 'Tanker'
    assert PD['General']['Origin'] == 'Magic'
    assert PD['General']['Server'] == 'Homecoming'
    assert PD['General']['Primary'] == 'Fiery Aura'
    assert PD['General']['Secondary'] == 'War Mace'
    assert PD['General']['Pool1'] == 'Flight'
    assert PD['General']['Pool2'] == 'Fighting'
    assert PD['General']['Pool3'] == 'Leadership'
    assert PD['General']['Epic'] == 'Soul Mastery'
    # and make sure we slurped in stuff from the Default Profile
    assert 'Sync' in PD['General']
    assert PD['General']['Sync'] == 'CTRL+S'
    assert 'QuitToSelect' in PD['General']
    assert PD['General']['QuitToSelect'] == 'CTRL+Q'

    assert PD.IsModified()

def test_MassageData(config, monkeypatch):
    monkeypatch.undo()
    rawdata = {
        'SoD' : {'DefaultMode' : 'No SoD'},
        'CustomBinds' : [
            {'Type' : 'BufferBind', 'BuffPower1' : 'Power1-1', 'BuffPower2' : 'Power1-2', 'BuffPower3' : 'Power1-3' },
            {'Type' : 'BufferBind', 'BuffPower1' : 'Power2-1', 'BuffPower2' : 'Power2-2', 'BuffPower3' : 'Power2-3' },
        ],
    }
    PD = ProfileData.ProfileData(config, newname = 'buffer', profiledata = rawdata)

    assert 'MovementPowers' in PD
    assert 'SoD' not in PD
    assert len(PD['CustomBinds']) == 2

    assert 'Buffs' in PD['CustomBinds'][0]
    assert len(PD['CustomBinds'][0]['Buffs']) == 3
    b = PD['CustomBinds'][0]['Buffs']
    assert b[0]['Power'] == 'Power1-1'
    assert b[1]['Power'] == 'Power1-2'
    assert b[2]['Power'] == 'Power1-3'

    assert 'Buffs' in PD['CustomBinds'][1]
    assert len(PD['CustomBinds'][1]['Buffs']) == 3
    b = PD['CustomBinds'][1]['Buffs']
    assert b[0]['Power'] == 'Power2-1'
    assert b[1]['Power'] == 'Power2-2'
    assert b[2]['Power'] == 'Power2-3'

def test_init_filename(tmp_path):

    profile_path = tmp_path / "testprofile.bcp"
    with pytest.raises(Exception, match = f'whose file "{profile_path}" is missing'):
        ProfileData.ProfileData(config, filename = str(profile_path))

    profile_path.write_text('{}')
    with pytest.raises(Exception, match = 'Something broke while loading'):
        ProfileData.ProfileData(config, filename = str(profile_path))

    profile_path.write_text('%#aflj BAD JSON BAD" $@!')
    with pytest.raises(Exception, match = 'Something broke while loading'):
        ProfileData.ProfileData(config, filename = str(profile_path))
    profile_path.unlink()

def test_accessors(config, monkeypatch, tmp_path, PD):

    assert PD.LastModTime     == PD.Filepath.stat().st_mtime_ns
    assert not PD.IsModified()
    assert PD.Server          == 'Rebirth'
    assert PD.ProfileName()   == 'testprofile'
    assert PD.ProfileIDFile() == PD.BindsDir() / 'bcprofileid.txt'
    assert PD.BindsDir()      == tmp_path / PD['ProfileBindsDir']
    assert PD.GameBindsDir()  == PureWindowsPath(tmp_path) / PD['ProfileBindsDir']

    monkeypatch.setattr(config, 'Read', lambda _: '')
    assert PD.GameBindsDir()  == PD.BindsDir()

def test_IsModified(PD):
    assert not PD.IsModified()
    PD['General']['Fubble'] = 'asdf'
    assert PD.IsModified()

# TODO TODO TODO - move this test somewhere else when we make a class for ProfileBindFiles or something
def test_GetBindFile(monkeypatch, PD):
    return
    resetfile = PD.ResetFile()
    assert resetfile == PD.GetBindFile('reset.txt')
    assert isinstance(resetfile, BindFile)

    otherbindfile = PD.GetBindFile('otherbindfile.txt')
    assert isinstance(otherbindfile, BindFile)
    assert otherbindfile              != resetfile
    assert otherbindfile.Path         == Path(PD.BindsDir()) / 'otherbindfile.txt'
    assert otherbindfile.GameBindsDir == PureWindowsPath(PD.BindsDir())
    assert otherbindfile.GamePath     == PureWindowsPath(otherbindfile.Path)

    monkeypatch.setattr(PD, 'GameBindsDir', lambda _: 'c:\\coh\\')
    posixbindfile = PD.GetBindFile('dir', 'posixbindfile.txt')
    assert posixbindfile.GamePath == PureWindowsPath('c:\\coh\\dir\\posixbindfile.txt')

def test_FillWith(PD):
    PD.FillWith({
        'ProfileBindsDir' : 'test_FillWith',
        'General'         : { 'Server' : 'Rebirth' },
    })

    assert PD.Server == 'Rebirth'
    assert PD['ProfileBindsDir'] == 'test_FillWith'
    assert 'MovementPowers' not in PD
    assert PD.IsModified()

def test_InspectData(PD):
    assert PD.InspectData('General', 'Origin') == 'Magic'

    PD.UpdateData('Testing', 'Updated', 'Thing')
    assert PD.InspectData('Testing', 'Updated') == 'Thing'

    PD.UpdateData('CustomBinds', { 'CustomID' : 1, 'Type' : 'SimpleBind' })
    bindlist = PD.InspectData('CustomBinds')
    assert isinstance(bindlist, list)
    assert len(bindlist) == 1

def test_UpdateData(PD):
    # updates existing data
    assert not PD.IsModified()

    PD.UpdateData('General', 'Primary', 'Fubble')
    assert PD['General']['Primary'] == 'Fubble'
    assert PD.IsModified()

    PD.UpdateData('General', 'Primary', 'Crab Spider Soldier')
    assert not PD.IsModified()

    # will create keys as needed
    PD.UpdateData('NewThing', 'MakeIt', 'Work')
    assert PD['NewThing']['MakeIt'] == 'Work'

    # will append new custom bind when empty
    PD.UpdateData('CustomBinds', { 'CustomID' : 1, 'Type' : 'SimpleBind' })
    assert len(PD['CustomBinds']) == 1
    assert PD['CustomBinds'][0]['CustomID'] == 1
    assert PD['CustomBinds'][0]['Type']     == 'SimpleBind'

    # will append new custom bind to existing
    PD.UpdateData('CustomBinds', { 'CustomID' : 2, 'Type' : 'SecondBind' })
    assert len(PD['CustomBinds']) == 2
    assert PD['CustomBinds'][1]['CustomID'] == 2
    assert PD['CustomBinds'][1]['Type']     == 'SecondBind'

    # will replace existing custom bind
    PD.UpdateData('CustomBinds', { 'CustomID' : 1, 'Type' : 'SomethingNew' })
    assert len(PD['CustomBinds']) == 2
    assert PD['CustomBinds'][0]['CustomID'] == 1
    assert PD['CustomBinds'][0]['Type']     == 'SomethingNew'

    # will delete a custom bind when asked
    PD.UpdateData('CustomBinds', { 'CustomID' : 1, 'Action' : 'delete' })
    assert len(PD['CustomBinds']) == 1
    assert PD['CustomBinds'][0]['CustomID'] == 2
    assert PD['CustomBinds'][0]['Type']     == 'SecondBind'

    PD.UpdateData('General', 'Stuff', '{"Primary" : "Ice Capades", "Secondary" : "Freestyle"}')
    assert PD['General']['Stuff']['Primary'] == 'Ice Capades'
    assert PD['General']['Stuff']['Secondary'] == 'Freestyle'

def test_HasPowerPool(PD):
    PD.UpdateData('General', 'Pool1', 'Flight')

    assert PD.HasPowerPool('Flight')
    assert not PD.HasPowerPool('Leprosy')

def test_HasPower(PD):
    PD.UpdateData('General', 'Pool1', 'Flight')
    PD.UpdateData('General', 'Pool1Powers', ['Fly', 'Hover'])
    PD.UpdateData('General', 'Primary', 'Test Powers')
    PD.UpdateData('General', 'PrimaryPowers', ['Test1', 'Test2'])
    PD.UpdateData('General', 'Secondary', 'No Powers Here')

    assert PD.HasPower('Flight', 'Hover')
    assert not PD.HasPower('Flight', 'Boeing')
    assert PD.HasPower('Test Powers', 'Test1')
    assert not PD.HasPower('Test Powers', 'Testosterone')
    assert PD.HasPower('No Powers Here', 'Picked No Powers')

def test_GetCustomID(PD):
    assert PD['MaxCustomID'] == 10
    newid = PD.GetCustomID()
    assert newid == 11
    assert PD['MaxCustomID'] == 11

def test_GenerateBindsDirectoryName(monkeypatch, PD):
    # Uses first letters of multiple words
    PD.Filepath = Path('Multiple Words Testing.bcp')
    assert PD.GenerateBindsDirectoryName() == 'mwt'

    # Tries to use capital letters
    PD.Filepath = Path('OneTestProfileName.bcp')
    assert PD.GenerateBindsDirectoryName() == 'otpn'

    # Trims to first five for longer names
    PD.Filepath = Path('Firsttest.bcp')
    assert PD.GenerateBindsDirectoryName() == 'first'

    PD.Filepath = Path('Check Again Multi Word.bcp')
    monkeypatch.setattr(Util.Paths, 'CheckProfileForBindsDir', lambda _,__: 'glamrock')
    assert PD.GenerateBindsDirectoryName() == ''
    monkeypatch.undo()

    # TODO - as mocked, this test doesn't actually test anything
    # but I've gone ahead and done it just for the sake of coverage
    monkeypatch.setattr(platform, 'system', lambda: 'Windows')
    monkeypatch.setattr(os.path, 'isreserved', lambda _: True, raising = False)
    PD.Filepath = Path('Profile Really Neat.bcp') # 'prn' is reserved
    assert PD.GenerateBindsDirectoryName() == 'profi'

def test_doSaveAsDefault(PD, config, DefaultProfile):
    config.Write('DefaultProfile', DefaultProfile)
    PD.doSaveAsDefault()
    assert config.Read('DefaultProfile') != DefaultProfile, "Saves a new Default Profile"

def test_GetDefaultProfileJSON(PD, config, DefaultProfile, monkeypatch):
    monkeypatch.undo() # get rid of "Read" monkeypatch on config
    config.Write('DefaultProfile', '%#aflj BAD JSON BAD" $@!')
    with pytest.raises(Exception, match = 'Problem loading default profile'):
        jsonstring = PD.GetDefaultProfileJSON()

    config.Write('DefaultProfile', DefaultProfile)
    jsonstring = PD.GetDefaultProfileJSON()
    assert jsonstring is not None

    profiledata = json.loads(jsonstring)
    assert 'General' in profiledata
    assert profiledata['ProfileBindsDir'] == 't2'

def test_BindsDirNotMine(monkeypatch, PD):
    # correctly returns False for unclaimed bindsdir
    assert bool(PD.BindsDirNotMine()) is False

    PD.BindsDir().mkdir(exist_ok = True)

    # correctly returns truthy / profile name if claimed by someone else
    idfile = PD.ProfileIDFile()
    idfile.touch()
    idfile.write_text('not my circus')
    assert PD.BindsDirNotMine() == 'not my circus'

    # correctly returns False for claimbed by me
    idfile.write_text(PD.ProfileName())
    assert bool(PD.BindsDirNotMine()) is False

    # correctly blows up if the Profile doesn't know its id file
    monkeypatch.setattr(PD, 'ProfileIDFile', lambda: None)
    with pytest.raises(Exception, match = 'not checking IDFile'):
        _ = PD.BindsDirNotMine()

    idfile.unlink()
    PD.BindsDir().rmdir()

def test_doSaveToFile(config, monkeypatch):
    PD = ProfileData.ProfileData(config, newname = "test")

    PD.doSaveToFile()
    if PD.Filepath: # thanks pyright
        assert PD.FileHasChanged() is False
        sleep(.01)
        PD.Filepath.touch()
        assert PD.FileHasChanged() is True

        PD.Filepath.unlink()
        assert PD.FileHasChanged() is False

        monkeypatch.setattr(PD, 'AsJSON', raises_exception)
        with pytest.raises(Exception, match = 'Problem saving to profile'):
            PD.doSaveToFile()
        monkeypatch.undo()

        PD.Filepath = None
        with pytest.raises(Exception, match = 'No Filepath set'):
            PD.doSaveToFile()


#########
def raises_exception(*args): raise(Exception)

@pytest.fixture(autouse = True)
def config(tmp_path, monkeypatch):
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    monkeypatch.setattr(config, 'Read', lambda _: str(tmp_path))
    yield config
    config.DeleteAll()

@pytest.fixture
def PD(config):
    fixtureprofile = Path(__file__).resolve().parent / 'fixtures' / 'testprofile.bcp'
    return ProfileData.ProfileData(config, filename = str(fixtureprofile))

# This is sorta ugly innit
@pytest.fixture
def DefaultProfile():
    return "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"
