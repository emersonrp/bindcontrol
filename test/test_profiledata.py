#!/usr/sbin/python
import wx
import os, platform
import pytest
import json
import Models.ProfileData as ProfileData
from unittest.mock import Mock
from pathlib import Path, PureWindowsPath
from BindFile import BindFile
from Util.DefaultProfile import DefaultProfile

def test_CheckProfileForBindsDir(tmp_path):
    _, config = doSetup(tmp_path)

    # CheckProfileForBindsDir
    pdir = tmp_path / 'fubble'
    pdir.mkdir(exist_ok = True)
    file = pdir / 'bcprofileid.txt'
    file.write_text('Mister Fubble')
    assert ProfileData.CheckProfileForBindsDir(config, 'fubble') == 'Mister Fubble'
    file.unlink()
    pdir.rmdir()

    config.DeleteAll()

def test_GetProfileFileForName(tmp_path):
    _, config = doSetup(tmp_path)

    # GetProfileFileForName
    file = tmp_path / 'fubble.bcp'
    file.write_text('freebird')
    assert str(ProfileData.GetProfileFileForName(config, 'fubble')) == f'{tmp_path}/fubble.bcp'
    file.unlink()

    config.DeleteAll()

def test_GetAllProfileBindsDirs(tmp_path):
    _, config = doSetup(tmp_path)

    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.mkdir(exist_ok = True)

    assert sorted(ProfileData.GetAllProfileBindsDirs(config)) == sorted(['inky', 'pinky', 'blinky', 'clyde'])

    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.rmdir()

    config.DeleteAll()

def test_ProfilePath(tmp_path):
    _, config = doSetup(tmp_path)

    assert ProfileData.ProfilePath(config) == tmp_path

    config.DeleteAll()

def test_ProfileData_init_neither(tmp_path):
    _, config = doSetup(tmp_path)

    with pytest.raises(Exception, match = 'neither filename nor newname'):
        ProfileData.ProfileData(config)

    config.DeleteAll()

def test_ProfileData_init_newname(tmp_path):
    _, config = doSetup(tmp_path)

    pd = ProfileData.ProfileData(config, newname = 'test')
    assert pd.Config             == config
    assert pd.Filepath           == ProfileData.ProfilePath(config) / 'test.bcp'
    assert pd['ProfileBindsDir'] == 'test'
    assert pd.Modified           == True

    config.DeleteAll()

def test_ProfileData_init_filename(tmp_path):
    _, config = doSetup(tmp_path)

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

    config.DeleteAll()

def test_ProfileData_accessors(tmp_path):
    _, config = doSetup(tmp_path)
    fixtureprofile, pd = GetFixtureProfile(config)

    assert pd.Filepath        == fixtureprofile
    assert pd.LastModTime     == fixtureprofile.stat().st_mtime_ns
    assert pd.Modified        == False
    assert pd.Server          == 'Rebirth'
    assert pd.ProfileName()   == 'testprofile'
    assert pd.ProfileIDFile() == pd.BindsDir() / 'bcprofileid.txt'
    assert pd.BindsDir()      == tmp_path / pd['ProfileBindsDir']
    assert pd.GameBindsDir()  == PureWindowsPath(tmp_path) / pd['ProfileBindsDir']

    config.Read = Mock(return_value = '')
    assert pd.GameBindsDir()  == pd.BindsDir()

    config.DeleteAll()

def test_ProfileData_GetBindFile(tmp_path):
    _, config = doSetup(tmp_path)
    _, pd     = GetFixtureProfile(config)

    resetfile = pd.ResetFile()
    assert resetfile == pd.GetBindFile('reset.txt')
    assert isinstance(resetfile, BindFile)

    otherbindfile = pd.GetBindFile('otherbindfile.txt')
    assert isinstance(otherbindfile, BindFile)
    assert otherbindfile              != resetfile
    assert otherbindfile.Path         == Path(pd.BindsDir()) / 'otherbindfile.txt'
    assert otherbindfile.GameBindsDir == PureWindowsPath(pd.BindsDir())
    assert otherbindfile.GamePath     == PureWindowsPath(otherbindfile.Path)

    pd.GameBindsDir = Mock(return_value = 'c:\\coh\\')
    posixbindfile = pd.GetBindFile('dir', 'posixbindfile.txt')
    assert posixbindfile.GamePath == PureWindowsPath('c:\\coh\\dir\\posixbindfile.txt')

    config.DeleteAll()

def test_FillWith(tmp_path):
    _, config = doSetup(tmp_path)
    _, pd     = GetFixtureProfile(config)

    pd.FillWith({
        'ProfileBindsDir' : 'test_FillWith',
        'General'         : { 'Server' : 'Homecoming' },
    })

    assert pd.Server == 'Homecoming'
    assert pd.ProfileBindsDir == 'test_FillWith'
    assert 'MovementPowers' not in pd
    assert pd.Modified is True

    config.DeleteAll()

def test_UpdateData(tmp_path):
    _, config = doSetup(tmp_path)
    _, pd     = GetFixtureProfile(config)

    # updates existing data
    pd.UpdateData('General', 'Primary', 'Fubble')
    assert pd['General']['Primary'] == 'Fubble'

    # will create keys as needed
    pd.UpdateData('NewThing', 'MakeIt', 'Work')
    assert pd['NewThing']['MakeIt'] == 'Work'

    # will append new custom bind when empty
    pd.UpdateData('CustomBinds', { 'CustomID' : 1, 'Type' : 'SimpleBind' })
    assert len(pd['CustomBinds']) == 1
    assert pd['CustomBinds'][0]['CustomID'] == 1
    assert pd['CustomBinds'][0]['Type']     == 'SimpleBind'

    # will append new custom bind to existing
    pd.UpdateData('CustomBinds', { 'CustomID' : 2, 'Type' : 'SecondBind' })
    assert len(pd['CustomBinds']) == 2
    assert pd['CustomBinds'][1]['CustomID'] == 2
    assert pd['CustomBinds'][1]['Type']     == 'SecondBind'

    # will replace existing custom bind
    pd.UpdateData('CustomBinds', { 'CustomID' : 1, 'Type' : 'SomethingNew' })
    assert len(pd['CustomBinds']) == 2
    assert pd['CustomBinds'][0]['CustomID'] == 1
    assert pd['CustomBinds'][0]['Type']     == 'SomethingNew'

    # TODO - test sending JSON in as a value to make sure it gets de-JSON'd

    config.DeleteAll()

def test_GetCustomID(tmp_path):
    _, config = doSetup(tmp_path)
    _, pd     = GetFixtureProfile(config)

    assert pd['MaxCustomID'] == 10
    newid = pd.GetCustomID()
    assert newid == 11
    assert pd['MaxCustomID'] == 11

    config.DeleteAll()

def test_GenerateBindsDirectoryName(tmp_path):
    _, config = doSetup(tmp_path)
    _, pd     = GetFixtureProfile(config)

    # Uses first letters of multiple words
    pd.Filepath = Path('Multiple Words Testing.bcp')
    assert pd.GenerateBindsDirectoryName() == 'mwt'

    # Tries to use capital letters
    pd.Filepath = Path('OneTestProfileName.bcp')
    assert pd.GenerateBindsDirectoryName() == 'otpn'

    # Trims to first five for longer names
    pd.Filepath = Path('Firsttest.bcp')
    assert pd.GenerateBindsDirectoryName() == 'first'

    # Doesn't use Windows reserved words
    if platform.system() == "Windows":
        pd.Filepath = Path('Profile Really Neat.bcp') # 'prn' is reserved
        assert pd.GenerateBindsDirectoryName() == 'profi'

    config.DeleteAll()

def test_GetDefaultProfileJSON(tmp_path):
    # don't use doSetup() here as we don't want the Mock
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    _, pd     = GetFixtureProfile(config)

    jsonstring = pd.GetDefaultProfileJSON()
    assert jsonstring is None

    config.Write('DefaultProfile', "SOME GIBBERISH")
    with pytest.raises(Exception):
        jsonstring = pd.GetDefaultProfileJSON()

    config.Write('DefaultProfile', DefaultProfile)
    jsonstring = pd.GetDefaultProfileJSON()
    assert jsonstring is not None

    profiledata = json.loads(jsonstring)
    assert 'General' in profiledata
    assert profiledata['ProfileBindsDir'] == 'defau'

    config.DeleteAll()

#########
def doSetup(tmp_path):
    app = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    config.Read = Mock(return_value = str(tmp_path))

    return app, config

def GetFixtureProfile(config):
    fixtureprofile = Path(os.path.abspath(__file__)).parent / 'fixtures' / 'testprofile.bcp'
    return fixtureprofile, ProfileData.ProfileData(config, filename = str(fixtureprofile))
