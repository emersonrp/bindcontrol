from pathlib import Path
from KeyBind import KeyBind
from collections import deque

class BindFile():

    def __init__(self, profile, *pathbits):
        self.BindsDir = profile.BindsDir()
        pathbits = (self.BindsDir, *pathbits)

        self.Path = Path(*pathbits)

        self.KeyBinds = {}

    def SetBind(self, keybind):

        if keybind.Key == "UNBOUND": return

        self.KeyBinds[keybind.Key] = keybind

        # TODO -- how to call out the 'reset file' object as special?
        # TODO 2 -- we don't? it should be the page's responsibility to
        # stash keybinds in multiple bindfiles?  Maybe?
        # if ($file eq $resetfile1 and $key eq $resetkey) {
            # $resetfile2->{$key} = $s
        # }

    # Windows path b/c the game will use it.
    def BaseReset(self):
        return f'bind_load_file {self.BindsDir}\\subreset.txt'

    # TODO - make "silent" an option, and the default
    def BLF(self):
        return f'bindloadfile {self.Path}'

    def Write(self, profile):
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

        output = ''
        for keybind in sortedKeyBinds:
            print(f"...binding {keybind}")
            output = output + self.KeyBinds[keybind].GetKeyBindString()

        try:
            self.Path.write_text(output)
        except Exception as e:
            print("Can't write to {self.Path}: {e}")
