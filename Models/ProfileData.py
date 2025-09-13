import wx # TODO TODO TODO REMOVE THIS WHEN POSSIBLE



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
        self.MaxCustomID     : int                 = 0
        self.LastModTime     : int                 = 0
        self.Server          : str                 = "Homecoming"

        # TODO what is actually going to go here?
        self.Pages : list = []

        # are we wanting to load this one from a file?
        if self.Filepath:
            if not self.Filepath.exists():
                raise Exception(f'Tried to load a Profile whose file "{self.Filepath}" is missing')
            if data := json.loads(self.Filepath.read_text()):
                self.FillWith(data)
                self.LastModTime = self.Filepath.stat().st_mtime_ns
            else:
                raise Exception(f'Something broke while loading profile "{self.Filepath}".  This is a bug.')

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

        else:
            raise Exception("Error: ProfileData requested with neither filename or newname.  This is a bug.")

        GameData.SetupGameData(self.Server)

        if newname:    self.SetModified()
        elif filename: self.ClearModified()

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

    def SetModified(self):
        self.Modified = True

    def ClearModified(self):
        self.Modified = False

    def GetCustomID(self):
        self.MaxCustomID = self.MaxCustomID + 1
        self.SetModified()
        return self.MaxCustomID

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
        try:
            # so much could go wrong.
            self.Filepath = None
            jsonstring = self.AsJSON(small = True)
            zipstring = codecs.encode(jsonstring.encode('utf-8'), 'zlib')
            b64string = base64.b64encode(zipstring).decode('ascii')

            self.Config.Write('DefaultProfile', b64string)
            self.Config.Flush()
        except Exception as e:
            # Let us know if it did
            wx.LogError(f"Failed to write default profile: {e}")

    def GetDefaultProfileJSON(self):
        jsonstring = None

        # If we have it already saved the new way
        if self.Config.HasEntry('DefaultProfile'):
            try:
                b64string = self.Config.Read('DefaultProfile')
                zipstring = base64.b64decode(b64string)
                jsonstring = codecs.decode(zipstring, 'zlib')
            except Exception as e:
                wx.LogError(f"Problem loading default profile: {e}")

        return jsonstring

    def doSaveToFile(self):

        ProfilePath(self.Config).mkdir( parents = True, exist_ok = True )

        if not self.Filepath:
            raise Exception(f"No Filename set in Profile {self.ProfileName()}!  Aborting save.")
        savefile = self.Filepath

        dumpstring = self.AsJSON()

        try:
            self.Config.Write('LastProfile', str(savefile))
            savefile.touch() # make sure there's one there.
            savefile.write_text(dumpstring)
            self.LastModTime = savefile.stat().st_mtime_ns
            wx.LogMessage(f"Wrote profile {savefile}")
            self.ClearModified()
        except Exception as e:
            wx.LogError(f"Problem saving to profile {savefile}: {e}")

    def AsJSON(self, small = False):
        savedata : Dict[str, Any] = {}
        savedata['ProfileBindsDir'] = self['ProfileBindsDir']
        savedata['MaxCustomID']     = self.MaxCustomID
        for page in self.Pages:
            pagename = type(page).__name__
            savedata[pagename] = {}
            if pagename == "CustomBinds": continue

#            for controlname, control in page.Ctrls.items():
#                # Save disabled controls' states, too, so as not to lose config
#                # if someone, say, turns on "disable self tell" with a bunch of custom colors defined
#
#                # look up what type of control it is to know how to extract its value
#                if isinstance(control, wx.DirPickerCtrl):
#                    value = control.GetPath()
#                elif isinstance(control, PowerPicker):
#                    value = {
#                        'power'    : control.GetLabel(),
#                        'iconfile' : control.IconFilename,
#                    }
#                elif isinstance(control, bcKeyButton):
#                    value = control.Key
#                elif isinstance(control, wx.Button):
#                    value = control.GetLabel()
#                elif isinstance(control, wx.ColourPickerCtrl) or isinstance(control, csel.ColourSelect):
#                    value = control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
#                elif isinstance(control, wx.Choice):
#                    # we used to save the numerical selection which could break if the contents
#                    # of a picker changed between runs, like, say, if new powersets appeared.
#                    # Save the string value instead
#                    value = ""
#                    sel = control.GetSelection()
#                    if (sel != wx.NOT_FOUND): value = control.GetString(sel)
#                elif isinstance(control, wx.StaticText):
#                    continue
#                else:
#                    value = control.GetValue()
#
#                savedata[pagename][controlname] = value
#
#            if isinstance(page, General):
#                savedata['Server'] = page.ServerPicker.GetString(page.ServerPicker.GetSelection())

        savedata['CustomBinds'] = []
        customPage = getattr(self, 'CustomBinds')
        # TODO - walking the sizer/widget tree like this is fragile.
        for pane in customPage.PaneSizer.GetChildren():
            bindui = pane.GetSizer().GetChildren()
            if bindui:
                bindpane = bindui[0].GetWindow()
                if bindpane:
                    savedata['CustomBinds'].append(bindpane.Serialize())

        if small:
            return json.dumps(savedata, separators = (',', ':'))
        else:
            return json.dumps(savedata, indent=2)

    def doLoadFromFile(self, pathname):
        try:
            self.clear()
            self.update(json.loads(Path(pathname).read_text()))
        except Exception as e:
            wx.LogError(f"Profile {pathname} could not be loaded: {e}")
            return False

        self.Filepath = Path(pathname)

        # if we're loading a profile from before when we stored the
        # ProfileBindsDir in it, generate one.
        if not self['ProfileBindsDir']:
            self['ProfileBindsDir'] = self.GenerateBindsDirectoryName()
            self.SetModified()

        wx.LogMessage(f"Loaded profile {pathname}")
        return True

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
        IDFile = self.ProfileIDFile()
        if IDFile:
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

    def WriteBindFiles(self):

        # write the ProfileID file that identifies this directory as "belonging to" this profile
        try:
            self.ProfileIDFile().write_text(self.ProfileName())
        except Exception as e:
            # TODO custom exception?
            raise Exception("Can't write Profile ID file {self.ProfileIDFile()}: {e}")

        # Start by making the bind to make the reset load itself.  This might get overridden with
        # more elaborate load strings in like MovementPowers, but this is the safety fallback

        config = self.Config
        resetfile = self.ResetFile()
        keybindreset = 'keybind_reset' if config.ReadBool('FlushAllBinds') else ''
        feedback = 't $name, Resetting keybinds.'
        resetfile.SetBind(config.Read('ResetKey'), "Reset Key", "Preferences", [keybindreset , feedback, resetfile.BLF()])

        errors = []
        donefiles = 0

        # Go to each page....
        for page in self.Pages:
            # ... and tell it to gather up binds and put them into bindfiles.
            try:
                success = page.PopulateBindFiles()
                if not success:
                    wx.LogMessage(f'An error on the "{page.TabTitle}" tab caused WriteBinds to fail.')
                    return
            except Exception as e:
                if config.ReadBool('CrashOnBindError'):
                    raise e
                else:
                    errors.append(f"Error populating bind file: {e}")

        # Now we have them here and can iterate them
        totalfiles = len(self.BindFiles)
        dlg = wx.ProgressDialog('Writing Bind Files','',
            maximum = totalfiles, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)

        for bindfile in self.BindFiles.values():
            try:
                bindfile.Write()
                donefiles += 1
            except Exception as e:
                if config.ReadBool('CrashOnBindError'):
                    raise e
                else:
                    errors.append(f"Failed to write bindfile {bindfile.Path}: {e}")

            dlg.Update(donefiles, str(bindfile.Path))

        dlg.Destroy()

        if errors:
            msg = f"{donefiles} of {totalfiles} bind files written.\n\nThere were {len(errors)} errors!  Check the log."
        else:
            msg = f"{donefiles} of {totalfiles} bind files written successfully."

        return (errors, msg)

    def AllBindFiles(self):
        files = [self.ResetFile()]
        dirs  = []
        for page in self.Pages:
            bf = page.AllBindFiles()
            for file in bf['files']:
                files.append(file)
            for bdir in bf['dirs']:
                dirs.append(bdir)

        return {
            'files' : files,
            'dirs'  : dirs,
        }

    def doDeleteBindFiles(self, bindfiles):

        bindpath = self.Config.Read('BindPath')
        if len(bindpath) < 6: # "C:\COH" being the classic
            # TODO custom exception?
            raise Exception(f"Your Binds Directory is set to '{bindpath}' which seems wrong.  Check the preferences dialog.", "Binds Directory Error", wx.OK)

        if not bindfiles:
            # TODO custom exception?
            raise Exception("Tried to doDeleteBindFiles with no bindfiles.  Please report this as a bug.  Bailing.")

        # bindfiles is generated using someone's AllBindFiles(), which uses
        # Profile.GetBindFile(), so if BindsDir is sane, we're probably OK.

        totalfiles = len(bindfiles['files']) + len(bindfiles['dirs'])
        dlg = wx.ProgressDialog('Deleting Bind Files', '',
            maximum = totalfiles, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)

        # try all 15k+ of the files
        progress = 0
        removed = 0
        for file in bindfiles['files']:
            if not file.Path.is_relative_to(bindpath):
                wx.LogWarning(f"Bindfile {file.Path} not in {bindpath}, skipping deletion!")
            elif file.Path.is_file():
                file.Path.unlink()
                removed = removed + 1

            dlg.Update(progress, str(file.Path))
            progress = progress + 1


        # remove the ProfileID file
        try:
            self.ProfileIDFile().unlink()
        except Exception as e:
            wx.LogMessage(f"Can't delete ProfileID file: {e}")

        # try the directories
        for bdir in bindfiles['dirs']:
            dirpath = Path(self.BindsDir() / bdir)
            if dirpath.is_dir():
                # try / except because if it's not empty it'll barf.
                try:
                    dirpath.rmdir()
                    # not incrementing "removed" here because we just want to count
                    # files, so we can match "wrote X files" with "deleted X files"
                    pass
                except Exception:
                    pass

            dlg.Update(progress, bdir)
            progress = progress + 1

        # remove the bindsdir itself, if empty
        bindsdir = Path(self.BindsDir())
        try:
            bindsdir.rmdir()
        except Exception:
            pass

        # clear out our state
        self.BindFiles = {}

        return removed
