import re, os, platform
from pathlib import PurePath, Path, PureWindowsPath
from typing import Dict, Any
import json
import codecs
import base64
import wx
import wx.lib.colourselect as csel

import GameData

from BindFile import BindFile
from BLF import BLF

from Icon import GetIcon

from Page.General import General
from Page.Gameplay import Gameplay
from Page.MovementPowers import MovementPowers
from Page.InspirationPopper import InspirationPopper
from Page.Mastermind import Mastermind
from Page.CustomBinds import CustomBinds
from Page.PopmenuEditor import PopmenuEditor

import UI
from UI.ControlGroup import cgSpinCtrl, cgSpinCtrlDouble
from UI.SimpleBindPane import SimpleBindPane
from UI.BufferBindPane import BufferBindPane
from UI.ComplexBindPane import ComplexBindPane
from UI.WizardBindPane import WizardBindPane
from UI.BindWizard import wizards
from UI.KeySelectDialog import bcKeyButton
from UI.PowerPicker import PowerPicker

# class method to examine an arbitrary profile binds dir for its associated profile name
def CheckProfileForBindsDir(bindsdir):
    IDFile = Path(wx.ConfigBase.Get().Read('BindPath')) / bindsdir / 'bcprofileid.txt'
    if IDFile:
        # If the file is even there...
        if IDFile.exists():
            return IDFile.read_text().strip()

# class method to get a Path object given a profile name
def GetProfileFileForName(name):
    file = Path(wx.ConfigBase.Get().Read('ProfilePath')) / f"{name}.bcp"
    return file if file.is_file() else None

# class method to get all profile binds dirs as a list of strings.
#
# Might want to case-mangle these in calling code if checking against them, but
# let's not do it inside here in case we want to touch them directly on Linux
# etc where changing the case inside here would be bad.
def GetAllProfileBindsDirs():
    alldirs = []
    for bindsdir in Path(wx.ConfigBase.Get().Read('BindPath')).glob('*'):
        if bindsdir.is_dir():
            alldirs.append(bindsdir.name)
    return alldirs

# class method to load a Profile from a file-open dialog
def LoadFromFile(parent):
    with wx.FileDialog(parent, "Open Profile file",
            wildcard   = "Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
            defaultDir = str(ProfilePath()),
            style      = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            wx.LogMessage("User canceled loading profile")
            return False     # the user changed their mind

        pathname = fileDialog.GetPath()

    with wx.WindowDisabler():
        _ = wx.BusyInfo(wx.BusyInfoFlags().Parent(parent).Text('Loading...'))
        wx.GetApp().Yield()

        if newProfile := Profile(parent, filename = pathname):
            newProfile.buildFromData()
            newProfile.CheckAllConflicts()
            return newProfile
        else:
            newProfile.Destroy()

# class method to return the current Profile Path
def ProfilePath():
    return Path(wx.ConfigBase.Get().Read('ProfilePath'))

class Profile(wx.Notebook):

    def __init__(self, parent, filename = None, newname = None):
        wx.Notebook.__init__(self, parent, style = wx.NB_TOP, name = "Profile")

        self.BindFiles       : dict      = {}
        self.Pages           : list      = []
        self.Modified        : bool      = False
        self.Filename        : Path|None = Path(filename) if filename else None
        self.ProfileBindsDir : str       = ''
        self.LastModTime     : int       = 0
        self.Server          : str       = 'Homecoming'

        self.Data = {}

        # are we wanting to load this one from a file?
        if self.Filename and self.Filename.exists():
            if data := json.loads(Path(self.Filename).read_text()):
                self.Data = data
                self.LastModTime = self.Filename.stat().st_mtime_ns
            else:
                raise Exception(f"Something broke while loading profile {self.Filename}.  This is a bug.")

        # No?  Then it ought to be a new profile, and we ought to have passed in a name
        elif newname:
            self.Filename = ProfilePath() / f"{newname}.bcp"
            jsonstring = self.GetDefaultProfileJSON()
            if jsonstring:
                if data := json.loads(jsonstring):
                    self.Data = data
                else:
                    raise Exception(f"Something broke while loading profile {self.Filename}.  This is a bug.")

            self.ProfileBindsDir = self.GenerateBindsDirectoryName()
            if not self.ProfileBindsDir:
                # This happens if GenerateBindsDirectoryName can't come up with something sane
                parent.OnProfDirButton()

        else:
            raise Exception("Error: Profile created with neither filename or newname.  This is a bug.")

        self.Server = self.Data.get('Server', 'Homecoming')
        GameData.SetupGameData(self.Server)

        # Add the individual tabs, in order.
        self.General           = self.CreatePage(General(self))
        self.CustomBinds       = self.CreatePage(CustomBinds(self))
        self.Gameplay          = self.CreatePage(Gameplay(self))
        self.MovementPowers    = self.CreatePage(MovementPowers(self))
        self.InspirationPopper = self.CreatePage(InspirationPopper(self))
        self.Mastermind        = self.CreatePage(Mastermind(self))
        self.PopmenuEditor     = self.CreatePage(PopmenuEditor(self))

        if newname:    self.SetModified()
        elif filename: self.ClearModified()

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, parent.OnPageChanged)

    def CreatePage(self, module):
        module.BuildPage()
        module.SetScrollRate(10,10)
        self.AddPage(module, module.TabTitle)

        modname = type(module).__name__

        self.Pages.append(modname)

        self.Layout()
        return module

    #####
    # Convenience / JIT accessors
    def ProfileName(self)   : return self.Filename.stem if self.Filename else ''
    def Archetype(self)     : return self.General.GetState('Archetype')
    def Primary(self)       : return self.General.GetState('Primary')
    def Secondary(self)     : return self.General.GetState('Secondary')
    def ResetFile(self)     : return self.GetBindFile("reset.txt")
    def ProfileIDFile(self) : return self.BindsDir() / 'bcprofileid.txt'
    def BindsDir(self)      : return Path(wx.ConfigBase.Get().Read('BindPath')) / self.ProfileBindsDir
    def GameBindsDir(self) :
        if gbp := wx.ConfigBase.Get().Read('GameBindPath'):
            return PureWindowsPath(gbp) / self.ProfileBindsDir
        else:
            return self.BindsDir()

    def HasPowerPool(self, poolname):
        for picker in ['Pool1', 'Pool2', 'Pool3', 'Pool4']:
            pctrl = self.General.Ctrls[picker]
            if (sel := pctrl.GetSelection()) != wx.NOT_FOUND:
                if pctrl.GetString(sel) == poolname:
                    return True
        return False

    def BLF(self, *args):
        filepath = self.GameBindsDir()
        for arg in args: filepath = filepath  /  arg
        return f"$${BLF()} " + str(filepath)

    def CheckConflict(self, key, existingctrlname):
        conflicts = []

        for pageName in self.Pages:
            page = getattr(self, pageName)
            for ctrlname, ctrl in page.Ctrls.items():
                if isinstance(ctrl, bcKeyButton):
                    if not ctrl.IsThisEnabled(): continue
                    if (key != '') and (key == ctrl.Key) and (not existingctrlname == ctrlname):
                        conflicts.append( {'page' : page.TabTitle, 'ctrl': UI.Labels[ctrlname]})
        return conflicts

    # check all buttons for conflicts.
    def CheckAllConflicts(self):
        for pageName in self.Pages:
            page = getattr(self, pageName)
            for _, ctrl in page.Ctrls.items():
                if isinstance(ctrl, bcKeyButton):
                    if not ctrl.IsThisEnabled(): continue
                    ctrl.CheckConflicts()

    def SetModified(self, _ = None):
        self.Parent.SetTitle(f"BindControl: {self.ProfileName()} (*)") # pyright: ignore
        self.Modified = True

    def ClearModified(self, _ = None):
        self.Parent.SetTitle(f"BindControl: {self.ProfileName()}") # pyright: ignore
        self.Modified = False

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
        existingProfile = CheckProfileForBindsDir(fallback)
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
            existingProfile = CheckProfileForBindsDir(bdc)
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
    def SaveAsDefault(self, prompt = True):
        if prompt:
            result = wx.MessageBox("This will set the current profile to be used as a template when making a new profile.  Continue?", "Save As Default", wx.YES_NO)
            if result == wx.NO: return

        try:
            # so much could go wrong.
            self.Filename = None
            jsonstring = self.AsJSON(small = True)
            zipstring = codecs.encode(jsonstring.encode('utf-8'), 'zlib')
            b64string = base64.b64encode(zipstring).decode('ascii')

            wx.ConfigBase.Get().Write('DefaultProfile', b64string)
            wx.ConfigBase.Get().Flush()
        except Exception as e:
            # Let us know if it did
            wx.LogError(f"Failed to write default profile: {e}")

    def GetDefaultProfileJSON(self):
        jsonstring = None

        # If we have it already saved the new way
        if wx.ConfigBase.Get().HasEntry('DefaultProfile'):
            try:
                b64string = wx.ConfigBase.Get().Read('DefaultProfile')
                zipstring = base64.b64decode(b64string)
                jsonstring = codecs.decode(zipstring, 'zlib')
            except Exception as e:
                wx.LogError(f"Problem loading default profile: {e}")

        return jsonstring

    def SaveToFile(self):
        try:
            ProfilePath().mkdir( parents = True, exist_ok = True )
        except Exception as e:
            wx.LogError(f"Can't make Profile path {ProfilePath()} - {e}.  Aborting Save.")
            return

        with wx.FileDialog(self, "Save Profile file",
                wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(ProfilePath()),
                defaultFile = self.ProfileName(),
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogMessage("User canceled saving new profile")
                return False    # the user changed their mind

            # Proceed with the file chosen by the user
            pathname = fileDialog.GetPath()
            if not re.search(r'\.bcp$', pathname, flags = re.I):
                pathname = pathname + '.bcp'

            # set up our innards to be the new file
            self.Filename = Path(pathname)
            self.ProfileBindsDir = self.GenerateBindsDirectoryName()
            if not self.ProfileBindsDir:
                # This happens if GenerateBindsDirectoryName can't come up with something sane
                self.Parent.OnProfDirButton() # pyright: ignore

            # save the new file
            self.doSaveToFile()

            # make sure we're all set up as whatever we just saved as
            self.doLoadFromFile(str(self.Filename))

    def doSaveToFile(self):
        if not self.Filename:
            return self.SaveToFile()

        ProfilePath().mkdir( parents = True, exist_ok = True )

        if not self.Filename:
            raise Exception(f"No Filename set in Profile {self.ProfileName()}!  Aborting save.")
        savefile = self.Filename

        dumpstring = self.AsJSON()

        try:
            # check that we haven't updated the file from another copy of BindControl
            if savefile.exists():
                if savefile.stat().st_mtime_ns > self.LastModTime:
                    result = wx.MessageBox(f"Profile file {savefile} has changed since last save.  Continuing may overwrite changes.  Continue?", "File Modified", wx.YES_NO)
                    if result == wx.NO: return

            wx.ConfigBase.Get().Write('LastProfile', str(savefile))
            savefile.touch() # make sure there's one there.
            savefile.write_text(dumpstring)
            self.LastModTime = savefile.stat().st_mtime_ns
            wx.LogMessage(f"Wrote profile {savefile}")
            self.ClearModified()
        except Exception as e:
            wx.LogError(f"Problem saving to profile {savefile}: {e}")

        # We do this on save because we might have done "Save As" and we're now a new file
        self.SetTitle()

    def AsJSON(self, small = False):
        savedata : Dict[str, Any] = {}
        savedata['ProfileBindsDir'] = self.ProfileBindsDir
        for pagename in self.Pages:
            savedata[pagename] = {}
            if pagename == "CustomBinds": continue

            page = getattr(self, pagename)
            for controlname, control in page.Ctrls.items():
                # Save disabled controls' states, too, so as not to lose config
                # if someone, say, turns on "disable self tell" with a bunch of custom colors defined

                # look up what type of control it is to know how to extract its value
                if isinstance(control, wx.DirPickerCtrl):
                    value = control.GetPath()
                elif isinstance(control, PowerPicker):
                    value = {
                        'power'    : control.GetLabel(),
                        'iconfile' : control.IconFilename,
                    }
                elif isinstance(control, bcKeyButton):
                    value = control.Key
                elif isinstance(control, wx.Button):
                    value = control.GetLabel()
                elif isinstance(control, wx.ColourPickerCtrl) or isinstance(control, csel.ColourSelect):
                    value = control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
                elif isinstance(control, wx.Choice):
                    # we used to save the numerical selection which could break if the contents
                    # of a picker changed between runs, like, say, if new powersets appeared.
                    # Save the string value instead
                    value = ""
                    sel = control.GetSelection()
                    if (sel != wx.NOT_FOUND): value = control.GetString(sel)
                elif isinstance(control, wx.StaticText):
                    continue
                else:
                    value = control.GetValue()

                savedata[pagename][controlname] = value

            if pagename == "General":
                savedata['Server'] = page.ServerPicker.GetString(page.ServerPicker.GetSelection())

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
            self.Data = json.loads(Path(pathname).read_text())
            self.buildFromData()
        except Exception as e:
            wx.LogError(f"Profile {pathname} could not be loaded: {e}")
            return False

        self.Filename = Path(pathname)

        # if we're loading a profile from before when we stored the
        # ProfileBindsDir in it, generate one.
        if not self.ProfileBindsDir:
            self.ProfileBindsDir = self.GenerateBindsDirectoryName()
            self.SetModified()

        wx.LogMessage(f"Loaded profile {pathname}")
        return True

    def buildFromData(self):
        self.SetTitle()

        self.MassageData()
        data = self.Data

        # we store the ProfileBindsDir outside of the sections
        if data and data.get('ProfileBindsDir', None):
            self.ProfileBindsDir = data['ProfileBindsDir']

        for pagename in ['General', 'Gameplay', 'MovementPowers', 'InspirationPopper', 'Mastermind', 'PopmenuEditor']:
            page = getattr(self, pagename)
            if data and pagename in data:
                for controlname, control in page.Ctrls.items():
                    value = None
                    if controlname in data[pagename]:
                        value = data[pagename].get(controlname, None)
                    # if we don't have a given control in the load data, skip it completely --
                    # it should already have the default value from Init
                    else: continue

                    # look up what type of control it is to know how to update its value
                    if isinstance(control, wx.DirPickerCtrl):
                        control.SetPath(value if value else '')
                    elif isinstance(control, PowerPicker):
                        control.SetLabel(value['power'])
                        if iconfile := value['iconfile']:
                            control.SetBitmap(GetIcon(iconfile))
                            control.IconFilename = iconfile
                        control.OnMenuSelection()
                    elif isinstance(control, wx.Button):
                        control.SetLabel(value if value else '')
                        if isinstance(control, bcKeyButton):
                            control.Key = value if value else ''
                    elif isinstance(control, wx.ColourPickerCtrl) or isinstance(control, csel.ColourSelect):
                        control.SetColour(value)
                        if isinstance(control, csel.ColourSelect):
                            wx.PostEvent(control, wx.CommandEvent(csel.EVT_COLOURSELECT.typeId, control.GetId()))
                    elif isinstance(control, wx.Choice):
                        # we used to save the numerical selection which could break if the contents
                        # of a picker changed between runs, like, say, if new powersets appeared.
                        # we still check whether we have a numerical value so we can load old profiles.
                        if isinstance(value, str):
                            value = control.FindString(value)
                            if value == wx.NOT_FOUND: value = 0
                        control.SetSelection(value if value else 0)
                    elif isinstance(control, wx.CheckBox):
                        control.SetValue(value if value else False)
                    elif isinstance(control, cgSpinCtrl) or isinstance(control, cgSpinCtrlDouble):
                        control.SetValue(value if value else page.Init.get(controlname, 0))
                    elif isinstance(control, wx.StaticText):
                        control.SetLabel(value if value else '')
                    else:
                        control.SetValue(value if value else '')

            page.SynchronizeUI()

            # Do this after SynchronizeUI for General because SynchronizeUI will blow away our powerset
            # picks when we re-fill those pickers from the archetype.
            if data and pagename == 'General':

                # Re-fill Primary and Secondary pickers, honoring old numeric indices if needed
                prim = data['General'].get('Primary', None)
                if isinstance(prim, str):
                    prim = page.Ctrls['Primary'].FindString(prim)
                page.Ctrls['Primary'].SetSelection(prim)

                seco = data['General'].get('Secondary', None)
                if isinstance(seco, str):
                    seco = page.Ctrls['Secondary'].FindString(seco)
                page.Ctrls['Secondary'].SetSelection(seco)

                epic = data['General'].get('Epic', None)
                if isinstance(epic, str):
                    epic = page.Ctrls['Epic'].FindString(epic)
                page.Ctrls['Epic'].SetSelection(epic)

                # And while we're in "General" make sure the "Server" picker is set right
                page.ServerPicker.SetSelection(page.ServerPicker.FindString(self.Server))

            page.Layout()

        cbpage = getattr(self, "CustomBinds")
        if data and cbpage:
            cbpage.scrolledPanel.DestroyChildren()
            cbpage.Ctrls = {}
            cbpage.Panes = []
            for custombind in data['CustomBinds']:
                if not custombind: continue

                bindpane = None
                if custombind['Type'] == "SimpleBind":
                    bindpane = SimpleBindPane(cbpage, init = custombind)
                elif custombind['Type'] == "BufferBind":
                    bindpane = BufferBindPane(cbpage, init = custombind)
                elif custombind['Type'] == "ComplexBind":
                    bindpane = ComplexBindPane(cbpage, init = custombind)
                elif custombind['Type'] == "WizardBind":
                    if wizClass := wizards.get(custombind['WizClass'], None):
                        bindpane = WizardBindPane(cbpage, wizClass, init = custombind)
                    else:
                        wx.LogError(f"Tried to load WizardBind with unknown class {custombind['WizClass']} - probably a bug!")

                if bindpane:
                    cbpage.AddBindToPage(bindpane = bindpane)


        # Finally, after loading all this stuff, THEN add the binds that toggle SetModified
        for pagename in ['General', 'Gameplay', 'MovementPowers', 'InspirationPopper', 'Mastermind', 'PopmenuEditor']:
            page = getattr(self, pagename)
            for evt in [
                wx.EVT_CHECKBOX, wx.EVT_BUTTON, wx.EVT_CHOICE, wx.EVT_COMBOBOX, wx.EVT_TEXT, wx.EVT_SPINCTRL,
                wx.EVT_DIRPICKER_CHANGED, wx.EVT_COLOURPICKER_CHANGED, wx.EVT_MENU, wx.EVT_RADIOBUTTON,
                wx.EVT_SLIDER,
            ]:

                page.Bind(evt, page.OnCommandEvent)

    # This is for mashing old legacy profiles into the current state of affairs.
    # Each step in here might eventually get deprecated but maybe not, there's
    # little downside to doing all of this forever.
    def MassageData(self):

        # load old Profiles pre-rename of "Movement Powers" tab
        if self.Data and 'SoD' in self.Data:
            self.Data['MovementPowers'] = self.Data['SoD']
            self.SetModified()

        # Massage old hardcoded-three-step BufferBinds into the new way
        if self.Data and 'CustomBinds' in self.Data:
            for i, custombind in enumerate(self.Data['CustomBinds']):
                if not custombind: continue

                if custombind.get('Type', '') == "BufferBind":
                    if power := custombind.get('BuffPower1', None):
                        self.SetModified()
                        custombind['Buffs'] = [{
                            'Power'   : power,
                            'ChatTgt' : custombind.get('BuffChat1Tgt', ''),
                            'Chat'    : custombind.get('BuffChat1', ''),
                        }]
                        del custombind['BuffPower1']
                        del custombind['BuffChat1Tgt']
                        del custombind['BuffChat1']

                    if power := custombind.get('BuffPower2', None):
                        self.SetModified()
                        custombind['Buffs'].append({
                            'Power'   : power,
                            'ChatTgt' : custombind.get('BuffChat2Tgt', ''),
                            'Chat'    : custombind.get('BuffChat2', ''),
                        })
                        del custombind['BuffPower2']
                        del custombind['BuffChat2Tgt']
                        del custombind['BuffChat2']

                    if power := custombind.get('BuffPower3', None):
                        self.SetModified()
                        custombind['Buffs'].append({
                            'Power'   : power,
                            'ChatTgt' : custombind.get('BuffChat3Tgt', ''),
                            'Chat'    : custombind.get('BuffChat3', ''),
                        })
                        del custombind['BuffPower3']
                        del custombind['BuffChat3Tgt']
                        del custombind['BuffChat3']

                    self.Data['CustomBinds'][i] = custombind

    def SetTitle(self):
        self.Parent.SetTitle(f"BindControl: {self.ProfileName()}") # pyright: ignore
        self.General.NameDisplay.SetLabel(self.ProfileName())
        self.General.Layout()

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
        if not self.ProfileBindsDir:
            wx.MessageBox("Profile Binds Directory is not valid, please correct this.")
            return

        # Create the BindsDir if it doesn't exist
        try:
            self.BindsDir().mkdir(parents = True, exist_ok = True)
        except Exception as e:
            wx.LogError("Can't make binds directory {self.BindsDir()}: {e}")
            wx.MessageBox("Can't make binds directory {self.BindsDir()}: {e}")
            return


        otherProfile = self.BindsDirNotMine()
        if otherProfile:
            # this directory belongs to someone else
            answer = wx.MessageBox(f"The binds directory {self.BindsDir()} contains binds from the profile \"{otherProfile}\" -- overwrite?", "Confirm", wx.YES_NO)
            if answer == wx.NO: return

        # write the ProfileID file that identifies this directory as "belonging to" this profile
        try:
            self.ProfileIDFile().write_text(self.ProfileName())
        except Exception as e:
            wx.LogError("Can't write Profile ID file {self.ProfileIDFile()}: {e}")
            wx.MessageBox("Can't write Profile ID file {self.ProfileIDFile()}: {e}")
            return

        # Start by making the bind to make the reset load itself.  This might get overridden with
        # more elaborate load strings in like MovementPowers, but this is the safety fallback

        config = wx.ConfigBase.Get()
        resetfile = self.ResetFile()
        keybindreset = 'keybind_reset' if config.ReadBool('FlushAllBinds') else ''
        feedback = 't $name, Resetting keybinds.'
        resetfile.SetBind(config.Read('ResetKey'), "Reset Key", "Preferences", [keybindreset , feedback, resetfile.BLF()])

        errors = 0
        donefiles = 0

        # Go to each page....
        for pageName in self.Pages:
            page = getattr(self, pageName)

            # ... and tell it to gather up binds and put them into bindfiles.
            try:
                success = page.PopulateBindFiles()
                if not success:
                    wx.LogMessage(f'An error on the "{pageName}" tab caused WriteBinds to fail.')
                    return
            except Exception as e:
                if config.ReadBool('CrashOnBindError'):
                    raise e
                else:
                    wx.LogMessage(f"Error populating bind file: {e}")
                    errors += 1

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
                    wx.LogMessage(f"Failed to write bindfile {bindfile.Path}: {e}")
                    errors += 1

            dlg.Update(donefiles, str(bindfile.Path))

        dlg.Destroy()

        if errors:
            msg = f"{donefiles} of {totalfiles} bind files written.\n\nThere were {errors} errors!  Check the log."
        else:
            msg = f"{donefiles} of {totalfiles} bind files written successfully."

        with WriteDoneDialog(self, msg = msg) as dlg:
            dlg.Show()
            dlg.Raise()
            dlg.ShowModal()
            if errors:
                wx.App.Get().Main.Logger.LogWindow.Show()

        # clear out our state
        self.BindFiles = {}

    def AllBindFiles(self):
        files = [self.ResetFile()]
        dirs  = []
        for pageName in self.Pages:
            page = getattr(self, pageName)
            bf = page.AllBindFiles()
            for file in bf['files']:
                files.append(file)
            for bdir in bf['dirs']:
                dirs.append(bdir)

        return {
            'files' : files,
            'dirs'  : dirs,
        }

    def DeleteBindFiles(self):
        result = wx.MessageBox((
                "DELETING ALL BINDFILES"
                "\n\n"
                "This will delete all BindControl-generated files and directories inside:"
                "\n\n"
                f"          {self.BindsDir()}"
                "\n\n"
                "Please double-check this path and make sure this is what you mean to do."
                "\n\n"
                "Are you sure?"
            ), "DELETE ALL BINDFILES", wx.YES_NO)
        if result == wx.NO: return

        removed = self.doDeleteBindFiles(self.AllBindFiles())

        if removed:
            with DeleteDoneDialog(self, removed = removed) as dlg:
                dlg.ShowModal()

    def doDeleteBindFiles(self, bindfiles):

        bindpath = wx.ConfigBase.Get().Read('BindPath')
        if len(bindpath) < 6: # "C:\COH" being the classic
            wx.MessageBox(f"Your Binds Directory is set to '{bindpath}' which seems wrong.  Check the preferences dialog.", "Binds Directory Error", wx.OK)
            return

        if not bindfiles:
            wx.LogError("Tried to doDeleteBindFiles with no bindfiles.  Please report this as a bug.  Bailing.")
            return

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

class WriteDoneDialog(wx.Dialog):
    def __init__(self, parent, msg = 'Bindfiles written.'):
        wx.Dialog.__init__(self, parent, title = "Bindfiles Written")

        sizer = wx.BoxSizer(wx.VERTICAL)

        msg = msg + (
            "\n\n"
            "You should now log on to the character you made\n"
            "them for and type or paste into the chat window:"
        )
        sizer.Add(
            wx.StaticText(self, label = msg, style = wx.ALIGN_CENTER),
            0, wx.EXPAND|wx.ALL, 10
        )

        ### helpful copyable /blf text
        blfSizer = wx.BoxSizer(wx.HORIZONTAL)
        textCtrl = wx.TextCtrl(self, id = wx.ID_ANY,
                       style = wx.TE_READONLY|wx.TE_CENTER,
                       value = "/bindloadfile " + str(parent.GameBindsDir() / "reset.txt")
        )
        textCtrl.SetFont(
            wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = 'Courier')
        )
        # https://wxpython.org/Phoenix/docs/html/wx.Control.html#wx.Control.GetSizeFromTextSize
        textCtrl.SetInitialSize(
            textCtrl.GetSizeFromTextSize(
                textCtrl.GetTextExtent(
                    textCtrl.GetValue()
                )
            )
        )
        blfSizer.Add(textCtrl, 1, wx.EXPAND)
        copyButton = wx.BitmapButton(self, bitmap = GetIcon('UI', 'copy'))
        copyButton.SetToolTip('Copy text')
        setattr(copyButton, 'textctrl', textCtrl)
        blfSizer.Add(copyButton, 0)
        copyButton.Bind(wx.EVT_BUTTON, self.doTextCopy)
        sizer.Add(blfSizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        ### "Files Written" list
        fileslist = wx.TextCtrl(self, id = wx.ID_ANY, size = wx.Size(-1, 150),
                                value = "reset.txt\n", style = wx.TE_READONLY|wx.TE_MULTILINE)
        for filename in sorted(parent.BindFiles.keys()):
            if filename == "reset.txt": continue
            bindfile = parent.BindFiles[filename]

            displaypath = bindfile.Path.relative_to(parent.BindsDir())

            fileslist.AppendText(f"{displaypath}\n")

        fileslist.SetInsertionPoint(0)

        sizer.Add(wx.StaticText(self, -1, label = "Files written:"), 0, wx.TOP|wx.RIGHT|wx.LEFT, 10)
        sizer.Add(fileslist, 0, wx.ALL|wx.EXPAND, 10)

        sizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizerAndFit(sizer)

    def doTextCopy(self, evt):
        dataObj = wx.TextDataObject(evt.EventObject.textctrl.GetValue())
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Couldn't open the clipboard for copying")

class DeleteDoneDialog(wx.Dialog):
    def __init__(self, parent, removed = 0):
        wx.Dialog.__init__(self, parent, title = "Bindfiles Deleted")

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(
            wx.StaticText(self, label = (
                    f"Deleted {removed} bind files and removed empty directories."
                    "\n\n"
                    "If you had previously loaded this set of binds with a character,"
                    "\n"
                    "you will likely experience bad results until you log into that character and type:"
                ), style = wx.ALIGN_CENTER),
            1, wx.EXPAND|wx.ALL, 10
        )
        textCtrl = wx.TextCtrl(self, id = wx.ID_ANY,
                       style = wx.TE_READONLY|wx.TE_CENTER,
                       value = "/keybind_reset",
        )
        textCtrl.SetFont(
            wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = 'Courier')
        )
        sizer.Add(textCtrl, 0, wx.EXPAND|wx.ALL, 10)

        sizer.Add(
            wx.StaticText(self, label = f"Alternatively, you can Write Binds again at this point for a fresh set of bindfiles.", style = wx.ALIGN_CENTER),
            0, wx.EXPAND|wx.ALL, 10
        )
        sizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.ALL|wx.ALIGN_RIGHT, 10)

        self.SetSizerAndFit(sizer)
