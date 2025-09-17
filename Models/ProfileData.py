import re, os, platform
from pathlib import PurePath, Path, PureWindowsPath
from typing import Dict, Any
import json
import codecs
import base64

import GameData

from BindFile import BindFile

# class method to examine an arbitrary profile binds dir for its associated profile name
def CheckProfileForBindsDir(config, bindsdir):
    IDFile = Path(config.Read('BindPath')) / bindsdir / 'bcprofileid.txt'
    if IDFile:
        # If the file is even there...
        if IDFile.exists():
            return IDFile.read_text().strip()

# class method to get a Path object given a profile name
def GetProfileFileForName(config, name):
    file = Path(config.Read('ProfilePath')) / f"{name}.bcp"
    return file if file.is_file() else None

# class method to get all profile binds dirs as a list of strings.
#
# Might want to case-mangle these in calling code if checking against them, but
# let's not do it inside here in case we want to touch them directly on Linux
# etc where changing the case inside here would be bad.
def GetAllProfileBindsDirs(config):
    alldirs = []
    for bindsdir in Path(config.Read('BindPath')).glob('*'):
        if bindsdir.is_dir():
            alldirs.append(bindsdir.name)
    return alldirs

# class method to return the current Profile Path
def ProfilePath(config): return Path(config.Read('ProfilePath'))

class ProfileData(dict):
    def __init__(self, config, filename = None, newname = None, profiledata = {}):

        if profiledata: self.FillWith(profiledata)

        self.Config                                = config # wx.Config object
        self.BindFiles       : Dict[str, BindFile] = {}
        self.Modified        : bool                = False
        self.Filepath        : Path|None           = Path(filename) if filename else None
        self.LastModTime     : int                 = 0
        self.Server          : str                 = "Homecoming"

        # are we wanting to load this one from a file?
        if self.Filepath:
            if not self.Filepath.exists():
                raise Exception(f'Tried to load a Profile whose file "{self.Filepath}" is missing')
            try:
                if data := json.loads(self.Filepath.read_text()):
                    self.FillWith(data)
                    self.LastModTime = self.Filepath.stat().st_mtime_ns
                else:
                    raise Exception(f'Something broke while loading profile "{self.Filepath}".  This is a bug.')
            except Exception:
                raise Exception(f'Something broke while loading profile "{self.Filepath}".  This is a bug.')

            self.ClearModified()
        # No?  Then it ought to be a new profile, and we ought to have passed in a name
        elif newname:
            self.Filepath = ProfilePath(self.Config) / f"{newname}.bcp"
            if jsonstring := self.GetDefaultProfileJSON():
                if data := json.loads(jsonstring):
                    self.FillWith(data)
                else:
                    raise Exception(f"Something broke while loading profile {self.Filepath}.  This is a bug.")

            self['ProfileBindsDir'] = self.GenerateBindsDirectoryName()
            if not self['ProfileBindsDir']:
                # This happens if GenerateBindsDirectoryName can't come up with something sane
                # # TODO TODO Throw a custom exception here, and catch it in Profile
                raise Exception("Can't come up with a sane Binds Directory!")

            self.SetModified()
        else:
            raise Exception("Error: ProfileData requested with neither filename nor newname.  This is a bug.")

        GameData.SetupGameData(self.Server)

    def ProfileName(self)   : return self.Filepath.stem if self.Filepath else ''
    def ResetFile(self)     : return self.GetBindFile("reset.txt")
    def ProfileIDFile(self) : return self.BindsDir() / 'bcprofileid.txt'
    def BindsDir(self)      : return Path(self.Config.Read('BindPath')) / self['ProfileBindsDir']
    def GameBindsDir(self) :
        if gbp := self.Config.Read('GameBindPath'):
            return PureWindowsPath(gbp) / self['ProfileBindsDir']
        else:
            return self.BindsDir()

    def FillWith(self, data):
        self.clear()
        self.update(data)
        self.Server          = self['General']['Server']
        self.SetModified()

    def UpdateData(self, pagename, *args):
        if pagename == 'CustomBinds':
            self[pagename] = self.get(pagename) or []
            replaced = False
            bindcontents = args[0]
            for i, testbind in enumerate(self[pagename]):
                if testbind['CustomID'] == bindcontents['CustomID']:
                    self[pagename][i] = bindcontents
                    replaced = True
                    break
            if not replaced:
                self[pagename].append(bindcontents)
        else:
            self[pagename] = self.get(pagename, {})
            # de-JSONize things if we got them from GetState().
            # This whole process wants revisiting.
            (ctlname, value) = args
            try:
                if value:
                    newvalue = json.loads(value)
                    if isinstance(newvalue, dict):
                        value = newvalue
            except Exception: pass # if it didn't JSON, just use it
            self[pagename][ctlname] = value
        self.SetModified()

    def SetModified(self):
        self.Modified = True

    def ClearModified(self):
        self.Modified = False

    def GetCustomID(self):
        self['MaxCustomID'] = self['MaxCustomID'] + 1
        self.SetModified()
        return self['MaxCustomID']

    # come up with a sane default binds directory name for this profile
    def GenerateBindsDirectoryName(self):
        bindsdircandidates = set()
        # start with just the ASCII a-zA-Z0-9_ and space characters in the name
        # We keep the spaces initially so the multi-word thing works at all.
        # TODO - This could cause trouble if someone has some weird all-Unicode name
        profileName = re.sub(r'[^\w ]+', '', self.ProfileName(), flags = re.ASCII)

        # First let's see if we have multiple words:
        namewords = profileName.split()
        if len(namewords) > 1 and len(namewords) < 6:
            firstletters = [w[:1] for w in namewords]
            bindsdircandidates.add(''.join(firstletters).lower())

        # let's see if we have more than one capital letter / numeral, if so try that.
        capitalletters = re.findall(r'[A-Z0-9]', profileName)
        if len(capitalletters) > 1 and len(capitalletters) < 6:
            bindsdircandidates.add(''.join(capitalletters).lower())

        # Let's also fall back on the first (non-space) five of the profileName as an option
        fallback = re.sub(r'\s+', '', profileName)[:5].lower()
        # ...if it's not already someone else's
        existingProfile = CheckProfileForBindsDir(self.Config, fallback)
        if existingProfile and (existingProfile != self.ProfileName()):
            fallback = ''

        # make a list() because we alter the bindsdircandidates set as we go
        for bdc in list(bindsdircandidates):
            # MSDOS still haunts us
            if platform.system() == "Windows" and os.path.isreserved(bdc): # pyright: ignore
                bindsdircandidates.remove(bdc)

            # if it's too short (1 character) let's not
            # This probably can't happen but sanity-checking is good
            if len(bdc) < 2: bindsdircandidates.remove(bdc)

            # check if it already exists and belongs to someone else
            existingProfile = CheckProfileForBindsDir(self.Config, bdc)
            if existingProfile and (existingProfile != self.ProfileName()):
                bindsdircandidates.remove(bdc)

        # OK, we should have zero, one, or two candidates of no more than five letters.
        # Pick the longest one; fall back on first-five if it was zero candidates
        #
        # We might still return '' if we just failed, so check for that in calling code.
        #
        # We're gonna lowercase this because Windows is case-insensitive
        return max(bindsdircandidates, key = len).lower() if bindsdircandidates else fallback

    ###################
    # Profile Save/Load
    def doSaveAsDefault(self):
        # if this blows up, calling code should try/except it
        self.Filepath = None
        jsonstring = self.AsJSON(small = True)
        zipstring = codecs.encode(jsonstring.encode('utf-8'), 'zlib')
        b64string = base64.b64encode(zipstring).decode('ascii')

        self.Config.Write('DefaultProfile', b64string)
        self.Config.Flush()

    def GetDefaultProfileJSON(self):
        jsonstring = None

        if self.Config.HasEntry('DefaultProfile'):
            try:
                b64string = self.Config.Read('DefaultProfile')
                zipstring = base64.b64decode(b64string)
                jsonstring = codecs.decode(zipstring, 'zlib')
            except Exception as e:
                raise Exception(f"Problem loading default profile: {e}")

        return jsonstring

    def doSaveToFile(self):

        ProfilePath(self.Config).mkdir( parents = True, exist_ok = True )

        if not self.Filepath:
            raise Exception(f"No Filename set in Profile {self.ProfileName()}!  Aborting save.")
        savefile = self.Filepath

        try:
            savefile.touch() # make sure there's one there.
            savefile.write_text(self.AsJSON())
            self.Config.Write('LastProfile', str(savefile))
            self.LastModTime = savefile.stat().st_mtime_ns
            self.ClearModified()
        except Exception as e:
            raise Exception(f"Problem saving to profile {savefile}: {e}")

    def AsJSON(self, small = False):
        if small:
            return json.dumps(self, separators = (',', ':'))
        else:
            return json.dumps(self, indent=2)

    #####################
    # Bind file functions
    def GetBindFile(self, *filebits):
        filepath = PurePath(*filebits)
        key = str(filepath)

        if not self.BindFiles.get(key, None):
            self.BindFiles[key] = BindFile(self.BindsDir(), self.GameBindsDir(), filepath)

        return self.BindFiles[key]

    # making this "not mine" so we can return False if everything's fine,
    # or the existing Profile name if something's wrong
    def BindsDirNotMine(self):
        if IDFile := self.ProfileIDFile():
            # If the file is even there...
            if IDFile.exists():
                profilename = IDFile.read_text().strip()

                if profilename == self.ProfileName():
                    # OK, this is our bindsdir, great
                    return False
                else:
                    # Oh noes someone else has written binds here, return the name
                    return profilename
            else:
                # the file doesn't exist, so bindsdir has not been claimed by another profile
                return False
        else:
            raise Exception("Profile.ProfileIDFile() returned nothing, not checking IDFile!")
