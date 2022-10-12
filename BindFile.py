from pathlib import Path, PureWindowsPath
from KeyBind import FileKeyBind
from collections import deque

class BindFile():

    def __init__(self, profile, *pathbits):

        self.BindsDir     = profile.BindsDir()
        self.Profile      = profile
        # TODO - check if GameBindsDir ends in \\, maybe in Profile itself?
        self.GameBindsDir = profile.GameBindsDir()

        filepathbits = (self.BindsDir, *pathbits)
        gamepathbits = (self.GameBindsDir, *pathbits)

        self.Path     = Path(*filepathbits)
        self.GamePath = PureWindowsPath(*gamepathbits)

        self.KeyBinds = {}

    def SetBind(self, keybind, contents = None):

        # TODO - this isinstance logic is here because SoD.py has about a million
        # spots where it just calls this with (key, string).  Better solution would be
        # to make SoD call this with a keybind object.

        # TODO and/or maybe this should just get called with key/string and
        # then forge its own KeyBind objects
        if isinstance(keybind, str):
            keybind = FileKeyBind(keybind, "", "", contents)

        if not keybind.Key: return

        self.KeyBinds[keybind.Key] = keybind

        # Terrible hack to add things into the subreset file when
        # added to the reset file.  Ouch.
        if self == self.Profile.ResetFile():
            subresetpath = Path(self.BindsDir) / "subreset.txt"
            subresetfile = self.Profile.GetBindFile(str(subresetpath))
            if keybind.Key != self.Profile.General.GetState('ResetKey'):
                subresetfile.SetBind(keybind, contents)

    # Windows path b/c the game will use it.
    def BaseReset(self):
        return f'bind_load_file {self.GameBindsDir}subreset.txt'

    # TODO - make "silent" an option, and the default
    def BLF(self):
        return f'bindloadfile {self.GamePath}'

    def Write(self):
        try:
            self.Path.parent.mkdir(parents = True, exist_ok = True)
        except Exception as e:
            print(f"Can't make parent dirs {self.Path.parent} : {e}")
            return

        try:
            self.Path.touch(exist_ok = True)
        except Exception as e:
            print(f"Can't instantiate file {self}: {e}")
            return

        # TODO -- sort all this stuff by the Alpha key, subsort by mod keys
        def rotateKeyBind(kb):
            kb = deque(kb.split('+'))
            kb.rotate(1)
            return "+".join(kb)
        sortedKeyBinds = sorted(self.KeyBinds, key = rotateKeyBind)
        # TODO this next line is just to imitate citbinder's weird naive sorting
        sortedKeyBinds = sorted(self.KeyBinds, key = str.casefold)

        output = ''
        for keybind in sortedKeyBinds:
            output = output + self.KeyBinds[keybind].GetKeyBindString()

        if output:
            try:
                self.Path.write_text(output, newline = '\r\n')
            except Exception as e:
                print("Can't write to {self.Path}: {e}")
