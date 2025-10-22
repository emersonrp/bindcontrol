import re
from typing import overload
from pathlib import PurePath, Path, PureWindowsPath
from BLF import BLF

class KeyBind:
    def __init__(self, key, name : str, page, contents : str|list[str]|None = None):
        contents = contents or []

        if type(contents) is str : contents = [contents]

        self.Key      : str       = key      # actual key combo
        self.Name     : str       = name     # friendly name, ie, "Select All Pets"
        self.Page     : str       = page     # which tab the bind originated on # pyright: ignore
        self.Contents : list[str] = contents # a list of strings to '$$'-join to create the actual payload # pyright: ignore

    # factory for PopulateBindFiles to use
    # TODO this should be a class method
    def MakeBind(self, contents):
        if type(contents) is str: contents = [contents]

        # changing self.Contents and reusing self over and over broke horribly in SoD.
        # Therefore, we just make a new KeyBind object.  Maybe investigate someday.
        return KeyBind(self.Key, self.Name, self.Page, contents)

    def BindString(self) -> str:
        payload = '$$'.join(i for i in self.Contents if i)

        # remove any initial $$ if we snuck in here with it.
        payload = re.sub(r'^\$\$', '', payload)
        # and any doubled up '$$'
        payload = re.sub(r'\$\$\$\$', '$$', payload)

        return payload

    def BindFileString(self) -> str:
        return f'{self.Key} "{self.BindString()}"\n'

class BindFile:

    def __init__(self, bindsdir, gamebindsdir, pathbits:PurePath):

        self.Path         = Path(bindsdir, pathbits)
        self.GameBindsDir = gamebindsdir
        self.GamePath     = PureWindowsPath(self.GameBindsDir, pathbits)

        self.KeyBinds = {}

    @overload
    def SetBind(self, keybind: KeyBind): ...
    @overload
    def SetBind(self, keybind: str, name: str, page, contents: str|list[str]): ...

    def SetBind(self, keybind:KeyBind|str, name:str = '', page = '', contents:str|list[str] = '') -> None:

        # we can either be called with a KeyBind, in which case we're golden, or with
        # four strings, in which case we need to roll a KeyBind.  Someday pick one scheme.
        if isinstance(keybind, str):
            keybind = KeyBind(keybind, name, page, contents)

        if not isinstance(page, str):
            page = page.TabTitle

        if not keybind.Key: return

        self.KeyBinds[keybind.Key] = keybind

    def BLF(self) -> str:
        return f'{BLF()} {self.GamePath}'

    def Write(self) -> None:
        try:
            self.Path.parent.mkdir(parents = True, exist_ok = True)
        except Exception as e:
            raise Exception(f"Can't make bindfile parent dirs {self.Path.parent} : {e}") from e

        try:
            self.Path.touch(exist_ok = True)
        except Exception as e:
            raise Exception(f"Can't instantiate bindfile {self}: {e}") from e

        # duplicate citybinder's (modified) logic exactly
        def getMainKey(testkey):
            mainkey = testkey or "UNBOUND"
            mainkey = mainkey.upper()
            mainkey = re.sub(r'LSHIFT', '', mainkey)
            mainkey = re.sub(r'RSHIFT', '', mainkey)
            mainkey = re.sub(r'SHIFT', '', mainkey)
            mainkey = re.sub(r'LCTRL', '', mainkey)
            mainkey = re.sub(r'RCTRL', '', mainkey)
            mainkey = re.sub(r'CTRL', '', mainkey)
            mainkey = re.sub(r'LALT', '', mainkey)
            mainkey = re.sub(r'RALT', '', mainkey)
            mainkey = re.sub(r'ALT', '', mainkey)
            mainkey = re.sub(r'\+', "", mainkey)
            if mainkey == '':
                rval = testkey
            else:
                rval = mainkey
            # this next line is so we sort by, say, "S" <-> "S        CTRL+S" <-> "S        ALT+S"
            # it's weird but that's how CityBinder did it and it seems to work.
            if testkey != mainkey: rval = rval + "        " + testkey
            return rval

        sortedKeyBinds = sorted(self.KeyBinds, key = getMainKey)

        output = ''
        for keybind in sortedKeyBinds:
            kb = self.KeyBinds[keybind]
            bindstring = kb.BindString()
            if len(bindstring) > 255:
                # TODO - make this a custom exception so we can handle it specially
                raise Exception(f"Bind '{kb.Key}' from page '{kb.Page.TabTitle}' is {len(bindstring)} characters long - this will cause badness in-game!")
            output = output + kb.BindFileString()

        if output:
            try:
                self.Path.write_text(output, newline = '\r\n')
            except Exception as e:
                raise Exception(f"Can't write to bindfile {self.Path}: {e}") from e

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
