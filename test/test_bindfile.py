from BindFile import KeyBind, BindFile
from pathlib import Path

def test_keybind():
    kb = KeyBind('A', 'Test A', object(), ['One', 'Two', 'Three'])
    assert kb.GetKeyBindString() == 'A "One$$Two$$Three"\n', "Keybind string is well-formed"

    kb2 = kb.MakeFileKeyBind(["First", "$$Second", "Third"])
    assert kb != kb2, "MakeFileKeyBind returns a new object"
    assert kb2.GetKeyBindString() == 'A "First$$Second$$Third"\n', "GetKeybindString correctly strips extra $$"

    kb3 = kb.MakeFileKeyBind("$$unbind_all$$up 1$$emote wave")
    assert kb3.GetKeyBindString() == 'A "unbind_all$$up 1$$emote wave"\n', "GetKeyBindString correctly strips leading $$"

def test_bindfile():
    bf = BindFile('/tmp', 'c:\\tmp', Path('test', 'test'))

    kb = KeyBind('A', 'Test A', object(), ['One', 'Two', 'Three'])
    bf.SetBind(kb)
    assert bf.KeyBinds['A'] == kb, "BindFile correctly sets KeyBinds from object"

    bf.SetBind('B', 'Test B', object(), "This is a test")
    assert isinstance(bf.KeyBinds['B'], KeyBind), "BindFile correctly creates KeyBind when SetBind called with strings"

    bf.Write()
    written_file = Path('/tmp','test','test')
    assert written_file.exists(), "BindFile correctly writes a file"

    contents = written_file.read_text()
    assert contents == 'A "One$$Two$$Three"\nB "This is a test"\n', "BindFile's contents are as expected"

    written_file.unlink()
