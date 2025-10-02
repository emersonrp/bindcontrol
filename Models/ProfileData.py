import re
import os
import platform
from pathlib import Path, PureWindowsPath
import copy
import json
import codecs
import base64

import GameData

import Util.Paths

# Custom exception for Profile to catch
class BindsDirectoryException(Exception): pass

class ProfileData(dict):
    def __init__(self, config, filename = None, newname = None, profiledata : dict|None = None, editdefault : bool = False) -> None:
        profiledata = profiledata or {}

        self.Config                      = config # wx.Config object
        self.Filepath        : Path|None = Path(filename) if filename else None
        self.LastModTime     : int       = 0
        self.Server          : str       = "Homecoming"
        self.SavedState      : dict|None = None

        # are we wanting to load this one from a file?
        if self.Filepath:
            if not self.Filepath.exists():
                raise Exception(f'Tried to load a Profile whose file "{self.Filepath}" is missing')
            try:
                if data := json.loads(self.Filepath.read_text()):
                    self.FillWith(data)
                    self.LastModTime = self.Filepath.stat().st_mtime_ns
                    self.SavedState = copy.deepcopy(dict(self))
                    self.MassageData()
                    if 'ProfileBindsDir' not in self:
                        self['ProfileBindsDir'] = self.GenerateBindsDirectoryName()
                else:
                    raise Exception(f'Unable to parse JSON from "{self.Filepath}".')
            except Exception as e:
                raise Exception(f'Something broke while loading profile "{self.Filepath}: {e}".') from e

        # No?  Then it ought to be a new profile, and we ought to have passed in a name
        elif newname or editdefault:
            if newname:
                self.Filepath = Util.Paths.ProfilePath(self.Config) / f"{newname}.bcp"
            else: # editing default
                self.Filepath = Path('DEFAULT PROFILE.bcp') # we use this just to set Profile.ProfileName()

            # First, mash the Default Profile in there, if it exists
            if jsonstring := self.GetDefaultProfileJSON():
                try:
                    data = json.loads(jsonstring)
                    self.FillWith(data)

                except Exception as e:
                    raise Exception("Something broke while loading Default Profile.  This is a bug.") from e

            # then, if we had profiledata from a buildfile, mash that on top
            # This feels uglier and uglier, and probably wants to be DRYed up somehow
            # TODO - a real buildfile will only have General, but we need everything to make
            # the tests run.  This is not great.
            if profiledata:
                for tab in profiledata:
                    if tab == 'CustomBinds':
                        self[tab] = self.get(tab, [])
                        for bind in profiledata[tab]:
                            self[tab].append(bind)
                    else:
                        self[tab] = self.get(tab, {})
                        for k,v in profiledata[tab].items():
                            self[tab][k] = v

            # set up the ProfileBindsDir
            if newname:
                self['ProfileBindsDir'] = self.GenerateBindsDirectoryName()

            # We do this in case the Default Profile they have saved needs massaging.
            # TODO maybe we want to detect that and re-save the Default Profile?
            # Maybe not.
            self.MassageData()

            if editdefault:
                self.SavedState = copy.deepcopy(dict(self))
        else:
            raise Exception("Error: ProfileData created with neither filename nor newname.  This is a bug.")

        if not self['ProfileBindsDir']:
            raise BindsDirectoryException("Can't come up with a sane Binds Directory!")

        GameData.SetupGameData(self.Server)

    def ProfileName(self)   -> str      : return self.Filepath.stem if self.Filepath else ''
    def ProfileIDFile(self) -> Path     : return self.BindsDir() / 'bcprofileid.txt'
    def BindsDir(self)      -> Path     : return Path(self.Config.Read('BindPath')) / self['ProfileBindsDir']
    def GameBindsDir(self)  -> Path     :
        if gbp := self.Config.Read('GameBindPath'):
            return PureWindowsPath(gbp) / self['ProfileBindsDir']
        else:
            return self.BindsDir()

    def FillWith(self, data) -> None:
        self.clear()
        self.update(data)
        # These next three lines are wacky and unclear.  We want:
        # 1) Get Server from General if it's there
        # 2) otherwise get it from top-level
        # 3) otherwise make it 'Homecoming'
        server = self.get('General', {}).get('Server', '')
        self.Server = server if server else self.get('Server', 'Homecoming')

    def UpdateData(self, pagename, *args) -> None:
        if pagename == 'CustomBinds':
            self[pagename] = self.get(pagename, [])
            replaced = False
            bindcontents = args[0]
            for i, testbind in enumerate(self[pagename]):
                if testbind['CustomID'] == bindcontents['CustomID']:
                    if bindcontents.get('Action') == 'delete':
                        del self[pagename][i]
                        replaced = True
                        break
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
                    if not isinstance(newvalue, str): # we transformed it somehow
                        value = newvalue
            except Exception: pass # if it didn't JSON, just use it
            self[pagename][ctlname] = value

    def IsModified(self): return (dict(self) != self.SavedState)

    def GetCustomID(self) -> int:
        self['MaxCustomID'] = self.get('MaxCustomID', 0) + 1
        return self['MaxCustomID']

    # come up with a sane default binds directory name for this profile
    def GenerateBindsDirectoryName(self) -> str:
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
        existingProfile = Util.Paths.CheckProfileForBindsDir(self.Config, fallback)
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
            existingProfile = Util.Paths.CheckProfileForBindsDir(self.Config, bdc)
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

    # This is for mashing old legacy profiles into the current state of affairs.
    # Each step in here might eventually get deprecated but maybe not, there's
    # little downside to doing all of this forever.
    def MassageData(self):

        # load old Profiles pre-rename of "Movement Powers" tab
        if 'SoD' in self:
            self['MovementPowers'] = self['SoD']
            del self['SoD']

        # This option got renamed for better clarity
        if ('MovementPowers' in self) and (self['MovementPowers'].get('DefaultMode') == 'No SoD'):
            self['MovementPowers']['DefaultMode'] = 'No Default SoD'

        # Massage old hardcoded-three-step BufferBinds into the new way
        if 'CustomBinds' in self:
            for i, custombind in enumerate(self['CustomBinds']):
                if not custombind: continue

                if custombind.get('Type') == "BufferBind":
                    if power := custombind.pop('BuffPower1'):
                        custombind['Buffs'] = [{
                            'Power'   : power,
                            'ChatTgt' : custombind.pop('BuffChat1Tgt', ''),
                            'Chat'    : custombind.pop('BuffChat1', ''),
                        }]
                    if power := custombind.pop('BuffPower2'):
                        custombind['Buffs'].append({
                            'Power'   : power,
                            'ChatTgt' : custombind.pop('BuffChat2Tgt', ''),
                            'Chat'    : custombind.pop('BuffChat2', ''),
                        })
                    if power := custombind.pop('BuffPower3'):
                        custombind['Buffs'].append({
                            'Power'   : power,
                            'ChatTgt' : custombind.pop('BuffChat3Tgt', ''),
                            'Chat'    : custombind.pop('BuffChat3', ''),
                        })

                    self['CustomBinds'][i] = custombind

    def doSaveAsDefault(self) -> None:
        # if this blows up, calling code should try/except it
        self.Filepath = None
        jsonstring = self.AsJSON(small = True)
        zipstring = codecs.encode(jsonstring.encode('utf-8'), 'zlib')
        b64string = base64.b64encode(zipstring).decode('ascii')

        self.Config.Write('DefaultProfile', b64string)
        self.Config.Flush()

    def GetDefaultProfileJSON(self) -> bytes|None:
        jsonstring = None

        if self.Config.HasEntry('DefaultProfile'):
            try:
                b64string = self.Config.Read('DefaultProfile')
                zipstring = base64.b64decode(b64string)
                jsonstring = codecs.decode(zipstring, 'zlib')
            except Exception as e:
                raise Exception(f"Problem loading default profile: {e}") from e

        return jsonstring

    def FileHasChanged(self) -> bool:
        if self.Filepath:
            if self.Filepath.exists():
                return self.Filepath.stat().st_mtime_ns > self.LastModTime
        return False

    def doSaveToFile(self) -> None:
        Util.Paths.ProfilePath(self.Config).mkdir( parents = True, exist_ok = True )

        if not self.Filepath:
            raise Exception(f"No Filepath set in Profile {self.ProfileName()}!  Aborting save.")
        savefile = self.Filepath

        try:
            savefile.touch() # make sure there's one there.
            savefile.write_text(self.AsJSON())
            self.Config.Write('LastProfile', str(savefile))
            self.LastModTime = savefile.stat().st_mtime_ns
            self.SavedState = copy.deepcopy(dict(self))
        except Exception as e:
            raise Exception(f"Problem saving to profile {savefile}: {e}") from e

    def AsJSON(self, small = False) -> str:
        if small:
            return json.dumps(self, separators = (',', ':'))
        else:
            return json.dumps(self, indent=2)

    # making this "not mine" so we can return falsie if everything's fine,
    # or the existing Profile name if something's wrong
    def BindsDirNotMine(self) -> str:
        if IDFile := self.ProfileIDFile():
            # If the file is even there...
            if IDFile.exists():
                profilename = IDFile.read_text().strip()

                if profilename == self.ProfileName():
                    # OK, this is our bindsdir, great
                    return ''
                else:
                    # Oh noes someone else has written binds here, return the name
                    return profilename
            else:
                # the file doesn't exist, so bindsdir has not been claimed by another profile
                return ''
        else:
            raise Exception("Profile.ProfileIDFile() returned nothing, not checking IDFile!")
