from BindFile import KeyBind, BindFile
from pathlib import Path
import pytest
import wx

def test_keybind():
    kb = KeyBind('A', 'Test A', '', ['One', 'Two', 'Three'])
    assert kb.BindFileString() == 'A "One$$Two$$Three"\n', "BindFileString output is well-formed"

    kb2 = kb.MakeBind(["First", "$$Second", "Third"])
    assert kb != kb2, "MakeBind returns a new object"
    assert kb2.BindFileString() == 'A "First$$Second$$Third"\n', "BindFileString correctly strips extra $$"

    kb3 = kb.MakeBind("$$unbind_all$$up 1$$emote wave")
    assert kb3.BindFileString() == 'A "unbind_all$$up 1$$emote wave"\n', "BindFileString correctly strips leading $$"

def test_bindfile_keybinds(bindfile):
    kb = KeyBind('A', 'Test A', '', ['One', 'Two', 'Three'])
    bindfile.SetBind(kb)
    assert bindfile.KeyBinds['A'] == kb, "BindFile correctly sets KeyBinds from object"

    bindfile.SetBind('B', 'Test B', '', "This is a test")
    assert isinstance(bindfile.KeyBinds['B'], KeyBind), "BindFile correctly creates KeyBind when SetBind called with strings"

def test_bindfile_write(bindfile, monkeypatch, tmp_path):
    bindfile.SetBind('A', 'Test A', '', ['One', 'Two', 'Three'])
    bindfile.SetBind('B', 'Test B', '', "This is a test")
    bindfile.SetBind('SHIFT', 'Shift Test', '', "Testing bare SHIFT")

    monkeypatch.setattr(Path, 'mkdir', raise_exception)
    with pytest.raises(Exception, match = 'bindfile parent dirs'):
        bindfile.Write()
    monkeypatch.undo()

    monkeypatch.setattr(Path, 'touch', raise_exception)
    with pytest.raises(Exception, match = 'instantiate bindfile'):
        bindfile.Write()
    monkeypatch.undo()

    monkeypatch.setattr(Path, 'write_text', raise_exception)
    with pytest.raises(Exception, match = 'write to bindfile'):
        bindfile.Write()
    monkeypatch.undo()

    bindfile.Write()

    written_file = Path(tmp_path, 'test', 'test')
    assert written_file.exists(), "BindFile correctly writes a file"
    assert written_file.read_text() == 'A "One$$Two$$Three"\nB "This is a test"\nSHIFT "Testing bare SHIFT"\n', "BindFile's contents are as expected"
    written_file.unlink()

    bindfile.SetBind('LONG', 'Long Bindstring', '', 300 * 'X')
    with pytest.raises(Exception, match = 'badness in-game'):
        bindfile.Write()

def test_blf(config, bindfile, monkeypatch):
    assert bindfile.BLF() == 'bindloadfilesilent c:\\tmp\\test\\test', 'BindFile.BLF returns correct path'

    monkeypatch.setattr(config, 'ReadBool', lambda _: True)
    assert bindfile.BLF() == 'bindloadfile c:\\tmp\\test\\test', 'BindFile.BLF honors "verbose blf" config'
    monkeypatch.undo()

#########
def raise_exception(): raise(Exception)

@pytest.fixture
def config():
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)

    yield config

    config.DeleteAll()

@pytest.fixture
def bindfile(tmp_path):
    bf = BindFile(tmp_path, 'c:\\tmp', Path('test', 'test'))

    return bf
