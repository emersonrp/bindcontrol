import re
import inspect
from typing import List, overload
from pathlib import PurePath, Path, PureWindowsPath
from BLF import BLF

class KeyBind():
    def __init__(self, key, name : str, page, contents : str|List[str] = []):

        if type(contents) == str : contents = [contents]

        self.Key      : str       = key      # actual key combo
        self.Name     : str       = name     # friendly name, ie, "Select All Pets"
        self.Page     : str       = page     # which tab the bind originated on # pyright: ignore
        self.Contents : List[str] = contents # a list of strings to '$$'-join to create the actual payload # pyright: ignore

    # factory for PopulateBindFiles to use
    def MakeFileKeyBind(self, contents):
        if type(contents) == str: contents = [contents]

        # changing self.Contents and reusing self over and over broke horribly in SoD.
        # Therefore, we just make a new KeyBind object.  Maybe investigate someday.
        return KeyBind(self.Key, self.Name, self.Page, contents)

    def BindString(self):
        payload = '$$'.join([i for i in self.Contents if i])

        # remove any initial $$ if we snuck in here with it.
        payload = re.sub(r'^\$\$', '', payload)
        # and any doubled up '$$'
        payload = re.sub(r'\$\$\$\$', '$$', payload)

        return payload

    def BindFileString(self):
        return f'{self.Key} "{self.BindString()}"\n'

class BindFile():

    def __init__(self, bindsdir, gamebindsdir, pathbits:PurePath):

        self.Path         = Path(bindsdir, pathbits)
        self.GameBindsDir = gamebindsdir
        self.GamePath     = PureWindowsPath(self.GameBindsDir, pathbits)

        self.KeyBinds = {}

    @overload
    def SetBind(self, keybind: KeyBind): ...
    @overload
    def SetBind(self, keybind: str, name: str, page: str, contents: str|List[str]): ...

    def SetBind(self, keybind:KeyBind|str, name:str = '', page:str = '', contents:str|List[str] = ''):

        # we can either be called with a KeyBind, in which case we're golden, or with
        # four strings, in which case we need to roll a KeyBind.  Someday pick one scheme.
        if isinstance(keybind, str):
            if name and not contents: # got called as (key, contents), this is bad.
                currframe = inspect.currentframe()
                if currframe:
                    prevFrame = currframe.f_back
                    if prevFrame:
                        (filen, line, funcn, _, _) = inspect.getframeinfo(prevFrame)
                        raise(Exception(f"SetBind called old way from {filen}, {funcn}, {line} -- PROBABLY BROKEN"))
            keybind = KeyBind(keybind, name, page, contents)

        if not keybind.Key: return

        self.KeyBinds[keybind.Key] = keybind

    def BaseReset(self):
        return f'{BLF()} {PureWindowsPath(self.GameBindsDir) / "reset.txt"}'

    def BLF(self):
        return f'{BLF()} {self.GamePath}'

    def Write(self):
        try:
            self.Path.parent.mkdir(parents = True, exist_ok = True)
        except Exception as e:
            raise Exception(f"Can't make bindfile parent dirs {self.Path.parent} : {e}")

        try:
            self.Path.touch(exist_ok = True)
        except Exception as e:
            raise Exception(f"Can't instantiate bindfile {self}: {e}")

        # duplicate citybinder's (modified) logic exactly
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
            bindstring = kb.BindString()
            if len(bindstring) > 255:
                raise Exception(f"Bind '{kb.Key}' from page '{kb.Page}' is {len(bindstring)} characters long - this will cause badness in-game!")
            output = output + kb.BindFileString()

        if output:
            try:
                self.Path.write_text(output, newline = '\r\n')
            except Exception as e:
                raise Exception("Can't write to bindfile {self.Path}: {e}")

    # delete the bindfile.  THIS DOES NOT ASK FOR CONFIRMATION
#    def Delete(self):
#        if not self.Path:
#            raise Exception(f"Trying to delete a bindfile with empty Path")
#        # TODO do we actually want to check existence?  We want to pass a bunch of possible
#        # files through here but they might not all be there, almost certainly some won't
#        if not self.Path.exists():
#            raise Exception(f"Trying to delete nonexistant bindfile {self}")
#        if not re.match(self.Profile.BindsDir(), str(self.Path)):
#            raise Exception(f"Trying to delete a bindfile {self} not in {self.Profile.BindsDir()}!")
#
#        # TODO do we need more sanity checking?  Probably
#        #self.Path.unlink()
#        print(f"Would be deleting BindFile {self}")
