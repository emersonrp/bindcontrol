#!/usr/sbin/python
import wx
import os, platform
import pytest
import json
import Models.ProfileData as ProfileData
from time import sleep
from unittest.mock import Mock
from pathlib import Path, PureWindowsPath
from BindFile import BindFile
from Util.DefaultProfile import DefaultProfile

def test_init_neither():
    with pytest.raises(Exception, match = 'neither filename nor newname'):
        ProfileData.ProfileData(config)

def test_init_newname(config):
    PD = ProfileData.ProfileData(config, newname = 'test')
    assert PD.Config             == config
    assert PD.Filepath           == ProfileData.ProfilePath(config) / 'test.bcp'
    assert PD['ProfileBindsDir'] == 'test'
    assert PD.Modified           == True

def test_init_filename(tmp_path):

    profile_path = tmp_path / "testprofile.bcp"
    with pytest.raises(Exception, match = f'whose file "{profile_path}" is missing'):
        ProfileData.ProfileData(config, filename = str(profile_path))

    profile_path.write_text('{}')
    with pytest.raises(Exception, match = f'Something broke while loading'):
        ProfileData.ProfileData(config, filename = str(profile_path))

    profile_path.write_text('%#aflj BAD JSON BAD" $@!')
    with pytest.raises(Exception, match = f'Something broke while loading'):
        ProfileData.ProfileData(config, filename = str(profile_path))
    profile_path.unlink()

def test_accessors(config, tmp_path, PD):

    assert PD.LastModTime     == PD.Filepath.stat().st_mtime_ns
    assert PD.Modified        == False
    assert PD.Server          == 'Rebirth'
    assert PD.ProfileName()   == 'testprofile'
    assert PD.ProfileIDFile() == PD.BindsDir() / 'bcprofileid.txt'
    assert PD.BindsDir()      == tmp_path / PD['ProfileBindsDir']
    assert PD.GameBindsDir()  == PureWindowsPath(tmp_path) / PD['ProfileBindsDir']

    config.Read = Mock(return_value = '')
    assert PD.GameBindsDir()  == PD.BindsDir()

def test_GetBindFile(PD):
    resetfile = PD.ResetFile()
    assert resetfile == PD.GetBindFile('reset.txt')
    assert isinstance(resetfile, BindFile)

    otherbindfile = PD.GetBindFile('otherbindfile.txt')
    assert isinstance(otherbindfile, BindFile)
    assert otherbindfile              != resetfile
    assert otherbindfile.Path         == Path(PD.BindsDir()) / 'otherbindfile.txt'
    assert otherbindfile.GameBindsDir == PureWindowsPath(PD.BindsDir())
    assert otherbindfile.GamePath     == PureWindowsPath(otherbindfile.Path)

    PD.GameBindsDir = Mock(return_value = 'c:\\coh\\')
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
    PD.UpdateData('General', 'Primary', 'Fubble')
    assert PD['General']['Primary'] == 'Fubble'

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


    # TODO - test sending JSON in as a value to make sure it gets de-JSON'd

def test_GetCustomID(PD):
    assert PD['MaxCustomID'] == 10
    newid = PD.GetCustomID()
    assert newid == 11
    assert PD['MaxCustomID'] == 11

def test_GenerateBindsDirectoryName(PD):
    # Uses first letters of multiple words
    PD.Filepath = Path('Multiple Words Testing.bcp')
    assert PD.GenerateBindsDirectoryName() == 'mwt'

    # Tries to use capital letters
    PD.Filepath = Path('OneTestProfileName.bcp')
    assert PD.GenerateBindsDirectoryName() == 'otpn'

    # Trims to first five for longer names
    PD.Filepath = Path('Firsttest.bcp')
    assert PD.GenerateBindsDirectoryName() == 'first'

    # Doesn't use Windows reserved words
    if platform.system() == "Windows":
        PD.Filepath = Path('Profile Really Neat.bcp') # 'prn' is reserved
        assert PD.GenerateBindsDirectoryName() == 'profi'

def test_GetDefaultProfileJSON(PD, config, monkeypatch):
    monkeypatch.undo() # get rid of "Read" monkeypatch on config
    config.Write('DefaultProfile', '%#aflj BAD JSON BAD" $@!')
    with pytest.raises(Exception):
        jsonstring = PD.GetDefaultProfileJSON()

    config.Write('DefaultProfile', DefaultProfile)
    jsonstring = PD.GetDefaultProfileJSON()
    assert jsonstring is not None

    profiledata = json.loads(jsonstring)
    assert 'General' in profiledata
    assert profiledata['ProfileBindsDir'] == 'defau'

def test_BindsDirNotMine(PD):
    # correctly returns False for unclaimed bindsdir
    assert PD.BindsDirNotMine() is False

    PD.BindsDir().mkdir(exist_ok = True)

    # correctly returns truthy / profile name if claimed by someone else
    idfile = PD.ProfileIDFile()
    idfile.touch()
    idfile.write_text('not my circus')
    assert PD.BindsDirNotMine() == 'not my circus'

    # correctly returns False for claimbed by me
    idfile.write_text(PD.ProfileName())
    assert PD.BindsDirNotMine() is False

    # correctly blows up if the Profile doesn't know its id file
    PD.ProfileIDFile = Mock(return_value = None)
    with pytest.raises(Exception, match = 'not checking IDFile'):
        _ = PD.BindsDirNotMine()

    idfile.unlink()
    PD.BindsDir().rmdir()

def test_FileHasChanged(config):
    PD = ProfileData.ProfileData(config, newname = "test")

    PD.doSaveToFile()
    if PD.Filepath: # thanks pyright
        assert PD.FileHasChanged() is False
        sleep(.01)
        PD.Filepath.touch()
        assert PD.FileHasChanged() is True

        PD.Filepath.unlink()
#########
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
    fixtureprofile = Path(os.path.abspath(__file__)).parent / 'fixtures' / 'testprofile.bcp'
    yield ProfileData.ProfileData(config, filename = str(fixtureprofile))
