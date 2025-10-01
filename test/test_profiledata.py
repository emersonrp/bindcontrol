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

def test_init_newname(config, DefaultProfile, monkeypatch):
    monkeypatch.undo()
    PD = ProfileData.ProfileData(config, newname = 'test')
    assert PD.Config             == config
    assert PD.Filepath           == Util.Paths.ProfilePath(config) / 'test.bcp'
    assert PD['ProfileBindsDir'] == 'test'
    assert PD.Modified

    monkeypatch.setattr(ProfileData.ProfileData, 'GenerateBindsDirectoryName', lambda _: '')
    with pytest.raises(Exception, match = 'sane Binds Directory'):
        ProfileData.ProfileData(config, newname = 'nobindsdir')
    monkeypatch.undo()

    assert PD.SavedState == dict(PD)

def test_defaultprofile(config, DefaultProfile, monkeypatch):
    monkeypatch.undo() # get rid of "Read" monkeypatch on config
    config.Write('DefaultProfile', DefaultProfile)
    # newname + no profiledata == use Default Profile
    PD = ProfileData.ProfileData(config, newname = 'test')
    assert PD['General']['Archetype'] == 'Blaster'
    assert PD['General']['Origin'] == 'Magic'
    assert PD['General']['Server'] == 'Homecoming'
    assert PD['General']['Primary'] == 'Archery'
    assert PD['General']['Secondary'] == 'Atomic Manipulation'

    monkeypatch.setattr(json, 'loads', raises_exception)
    with pytest.raises(Exception, match = 'while loading Default Profile'):
        ProfileData.ProfileData(config, newname = 'explode')

    assert PD.SavedState == dict(PD)

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

    assert PD.SavedState == dict(PD)

def test_MassageData(config):
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
    assert not PD.Modified
    assert PD.Server          == 'Rebirth'
    assert PD.ProfileName()   == 'testprofile'
    assert PD.ProfileIDFile() == PD.BindsDir() / 'bcprofileid.txt'
    assert PD.BindsDir()      == tmp_path / PD['ProfileBindsDir']
    assert PD.GameBindsDir()  == PureWindowsPath(tmp_path) / PD['ProfileBindsDir']

    monkeypatch.setattr(config, 'Read', lambda _: '')
    assert PD.GameBindsDir()  == PD.BindsDir()

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
        'General'         : { 'Server' : 'Homecoming' },
    })

    assert PD.Server == 'Homecoming'
    assert PD['ProfileBindsDir'] == 'test_FillWith'
    assert 'MovementPowers' not in PD
    assert PD.Modified is True

def test_UpdateData(PD):
    # updates existing data
    assert not PD.Modified

    PD.UpdateData('General', 'Primary', 'Fubble')
    assert PD['General']['Primary'] == 'Fubble'
    assert PD.Modified

    PD.UpdateData('General', 'Primary', 'Crab Spider Soldier')
    assert not PD.Modified

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
    assert profiledata['ProfileBindsDir'] == 'nd'

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

        monkeypatch.setattr(PD, 'ClearModified', raises_exception)
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
