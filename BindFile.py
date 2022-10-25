import wx
import inspect
from pathlib import Path, PureWindowsPath
from KeyBind import FileKeyBind
from Page import Page
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

    def SetBind(self, keybind: FileKeyBind|str, name:str = '', page:Page|None = None, contents: str|list = ''):

        # we can either be called with a FileKeyBind, in which case we're golden, or with
        # four strings, in which case we need to roll a FileKeyBind.  Someday pick one scheme.
        if isinstance(keybind, str):
            if name and not contents: # got called as (key, contents), this is bad.
                prevFrame = inspect.currentframe().f_back
                (filen, line, funcn, _, _) = inspect.getframeinfo(prevFrame)
                print(f"SetBind called old way from {filen}, {funcn}, {line} -- PROBABLY BROKEN")
            keybind = FileKeyBind(keybind, name, page, contents)

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

        output = ''
        for keybind in sortedKeyBinds:
            kb = self.KeyBinds[keybind]
            payload = kb.GetKeyBindString()
            try:
                if len(payload) > 255: raise Exception
            except Exception as e:
                wx.LogError(f"Bind '{kb.Key}' from page '{kb.Page}' is too long - this will cause badness in-game!")
            finally:
                output = output + payload

        if output:
            try:
                self.Path.write_text(output, newline = '\r\n')
            except Exception as e:
                wx.LogError("Can't write to bindfile {self.Path}: {e}")

