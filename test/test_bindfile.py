from BindFile import KeyBind, BindFile

def test_keybind():
    kb = KeyBind('A', 'Test A', object(), ['One', 'Two', 'Three'])
    assert kb.GetKeyBindString() == 'A "One$$Two$$Three"\n', "Keybind string is well-formed"

    kb2 = kb.MakeFileKeyBind(["First", "$$Second", "Third"])
    assert kb != kb2, "MakeFileKeyBind returns a new object"
    assert kb2.GetKeyBindString() == 'A "First$$Second$$Third"\n', "GetKeybindString correctly strips extra $$"

    kb3 = kb.MakeFileKeyBind("$$unbind_all$$up 1$$emote wave")
    assert kb3.GetKeyBindString() == 'A "unbind_all$$up 1$$emote wave"\n', "GetKeyBindString correctlt strips leading $$"
