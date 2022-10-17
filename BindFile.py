import wx
import inspect
from pathlib import Path, PureWindowsPath
from KeyBind import FileKeyBind
#from collections import deque

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
            prevFrame = inspect.currentframe().f_back
            (filen, line, funcn, _, _) = inspect.getframeinfo(prevFrame)
            print(f"Called as string from {filen}, {funcn}, {line}")
            keybind = FileKeyBind(keybind, "", "", contents)

        if not keybind.Key: return

        self.KeyBinds[keybind.Key] = keybind

        # Terrible hack to add things into the subreset file when
        # added to the reset file.  Ouch.
        config = wx.ConfigBase.Get()
        if self == self.Profile.ResetFile():
            subresetpath = Path(self.BindsDir) / "subreset.txt"
            subresetfile = self.Profile.GetBindFile(str(subresetpath))
            if keybind.Key != config.Read('ResetKey'):
                subresetfile.SetBind(keybind, contents)

    # Windows path b/c the game will use it.
    def BaseReset(self):
        return f'bindloadfile {self.GameBindsDir}subreset.txt'

    # TODO - make "silent" an option, and the default
    def BLF(self):
        return f'bindloadfile {self.GamePath}'

    def Write(self):
        try:
            self.Path.parent.mkdir(parents = True, exist_ok = True)
        except Exception as e:
            wx.LogError(f"Can't make bindfile parent dirs {self.Path.parent} : {e}")
            return

        try:
            self.Path.touch(exist_ok = True)
        except Exception as e:
            wx.LogError(f"Can't instantiate bindfile {self}: {e}")
            return

        # duplicate citybinder's (modified) logic exactly
        import re
        def getMainKey(testkey):
            str = testkey or "UNBOUND"
            str = str.upper()
            str = re.sub(r'LSHIFT', '', str)
            str = re.sub(r'RSHIFT', '', str)
            str = re.sub(r'SHIFT', '', str)
            str = re.sub(r'LCTRL', '', str)
            str = re.sub(r'RCTRL', '', str)
            str = re.sub(r'CTRL', '', str)
            str = re.sub(r'LALT', '', str)
            str = re.sub(r'RALT', '', str)
            str = re.sub(r'ALT', '', str)
            str = re.sub(r'\+', "", str)
            if str == '':
                rval = testkey
            else:
                rval = str
            if testkey != str: rval = rval + "        " + testkey
            return rval
        sortedKeyBinds = sorted(self.KeyBinds, key = getMainKey)

        # TODO -- put this back when we're no longer diffing
#        def rotateKeyBind(kb):
#            kb = deque(kb.split('+'))
#            kb.rotate(1)
#            # turn them into, eg, 'S        +SHIFT' so "SHIFT-S" sorts after "S" but before "SPACE"
#            kb[0] = kb[0]+"        "
#            return "+".join(kb)
#        sortedKeyBinds = sorted(self.KeyBinds, key = rotateKeyBind)

        output = ''
        for keybind in sortedKeyBinds:
            kb = self.KeyBinds[keybind]
            payload = kb.GetKeyBindString()
            try:
                if len(payload) > 255:
                    raise Exception
            except Exception as e:
                wx.LogError(f"Bind '{kb.Key}' from page '{kb.Page}' is too long - this will cause badness in-game!")
            finally:
                output = output + payload

        if output:
            try:
                self.Path.write_text(output, newline = '\r\n')
            except Exception as e:
                wx.LogError("Can't write to bindfile {self.Path}: {e}")

