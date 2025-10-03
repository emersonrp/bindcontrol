#!/usr/sbin/python
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

def test_init_empty(config):
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

def test_init_filename(config, tmp_path):

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
    PD.UpdateData('General', 'Pool1Powers', ['Fly', 'Hover'])
    PD.UpdateData('General', 'PrimaryPowers', ['Test1', 'Test2'])

    assert PD.HasPower('Pool', 'Hover')
    assert not PD.HasPower('Pool', 'Boeing')
    assert PD.HasPower('Primary', 'Test1')
    assert not PD.HasPower('Primary', 'Testosterone')

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

        monkeypatch.setattr(PD, 'AsJSON', raises_exception)
        with pytest.raises(Exception, match = 'Problem saving to profile'):
            PD.doSaveToFile()
        monkeypatch.undo()

        PD.Filepath = None
        with pytest.raises(Exception, match = 'No Filepath set'):
            PD.doSaveToFile()


#########
def raises_exception(*args): raise(Exception)
