from BindFile import KeyBind, BindFile
from pathlib import Path

def test_keybind():
    kb = KeyBind('A', 'Test A', '', ['One', 'Two', 'Three'])
    assert kb.BindFileString() == 'A "One$$Two$$Three"\n', "BindFileString output is well-formed"

    kb2 = kb.MakeBind(["First", "$$Second", "Third"])
    assert kb != kb2, "MakeBind returns a new object"
    assert kb2.BindFileString() == 'A "First$$Second$$Third"\n', "BindFileString correctly strips extra $$"

    kb3 = kb.MakeBind("$$unbind_all$$up 1$$emote wave")
    assert kb3.BindFileString() == 'A "unbind_all$$up 1$$emote wave"\n', "BindFileString correctly strips leading $$"

def test_bindfile():
    bf = BindFile('/tmp', 'c:\\tmp', Path('test', 'test'))

    kb = KeyBind('A', 'Test A', '', ['One', 'Two', 'Three'])
    bf.SetBind(kb)
    assert bf.KeyBinds['A'] == kb, "BindFile correctly sets KeyBinds from object"

    bf.SetBind('B', 'Test B', '', "This is a test")
    assert isinstance(bf.KeyBinds['B'], KeyBind), "BindFile correctly creates KeyBind when SetBind called with strings"

    bf.Write()
    written_file = Path('/tmp','test','test')
    assert written_file.exists(), "BindFile correctly writes a file"

    contents = written_file.read_text()
    assert contents == 'A "One$$Two$$Three"\nB "This is a test"\n', "BindFile's contents are as expected"

    written_file.unlink()
