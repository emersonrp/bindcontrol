import re
from functools import partial
from pathlib import PurePath, Path, PureWindowsPath
from typing import Dict, List
import wx

import GameData

from Models.ProfileData import ProfileData

from BindFile import BindFile
from BLF import BLF

from Icon import GetIcon

from Page import Page as bcPage
from Page.General import General
from Page.Gameplay import Gameplay
from Page.MovementPowers import MovementPowers
from Page.InspirationPopper import InspirationPopper
from Page.Mastermind import Mastermind
from Page.CustomBinds import CustomBinds
from Page.PopmenuEditor import PopmenuEditor

import UI
from UI.SimpleBindPane import SimpleBindPane
from UI.BufferBindPane import BufferBindPane
from UI.ComplexBindPane import ComplexBindPane
from UI.WizardBindPane import WizardBindPane
from UI.BindWizard import wizards
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinder import EVT_POWERBINDER_CHANGED
from UI.PowerPicker import EVT_POWER_CHANGED

from Util.Paths import ProfilePath

class Profile(wx.Notebook):

    # class method to load a Profile from a file-open dialog
    @classmethod
    def LoadFromFile(cls, parent):
        config = wx.ConfigBase.Get()
        with wx.FileDialog(parent, "Open Profile file",
                wildcard   = "BindControl Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(ProfilePath(config)),
                style      = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogMessage("User canceled loading profile")
                return False     # the user changed their mind

            pathname = fileDialog.GetPath()

        with wx.WindowDisabler():
            _ = wx.BusyInfo(wx.BusyInfoFlags().Parent(parent).Text('Loading...'))
            wx.GetApp().Yield()

            return Profile.doLoadFromFile(parent, pathname)

    @classmethod
    def doLoadFromFile(cls, parent, pathname):
        newProfile = None
        if newProfile := Profile(parent, filename = pathname):
            newProfile.buildUIFromData()
            newProfile.CheckAllConflicts()

        return newProfile

    # Instance methods
    def __init__(self, parent, filename = None, newname = None, profiledata = None):
        super().__init__(parent, style = wx.NB_TOP, name = "Profile")

        self.Data            : ProfileData         = ProfileData(wx.ConfigBase.Get(), filename, newname, profiledata)
        self.BindFiles       : Dict[str, BindFile] = {}
        self.Pages           : List[bcPage]        = []
        self.Modified        : bool                = False
        self.Filepath        : Path|None           = Path(filename) if filename else None
        self.ProfileBindsDir : str                 = ''
        self.LastModTime     : int                 = 0

        GameData.SetupGameData(self.Server())

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

    def CreatePage(self, page):
        page.BuildPage()
        page.SetScrollRate(10,10)
        self.AddPage(page, page.TabTitle)

        self.Pages.append(page)

        self.Layout()
        return page

    #####
    # Convenience / JIT accessors
    def ProfileName(self)   : return self.Filepath.stem if self.Filepath else ''
    def Archetype(self)     : return self.General.GetState('Archetype')
    def Primary(self)       : return self.General.GetState('Primary')
    def Secondary(self)     : return self.General.GetState('Secondary')
    def ResetFile(self)     : return self.GetBindFile("reset.txt")
    def ProfileIDFile(self) : return self.BindsDir() / 'bcprofileid.txt'
    def Server(self)        : return self.Data.Server
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

    def GetCustomID(self) -> int: return self.Data.GetCustomID()

    def BLF(self, *args):
        filepath = self.GameBindsDir()
        for arg in args: filepath = filepath  /  arg
        return f"$${BLF()} " + str(filepath)

    def CheckConflict(self, key, existingctrlname):
        conflicts = []

        for page in self.Pages:
            for ctrlname, bindkey in page.GetKeyBinds():
                if (key != '') and (key == bindkey) and (not existingctrlname == ctrlname):
                    conflicts.append({'page' : page.TabTitle, 'ctrl' : UI.Labels.get(ctrlname, ctrlname)})

        # Explicit check against Reset Kay from Prefs dialog
        if (key != '') and (key == wx.ConfigBase.Get().Read('ResetKey') and existingctrlname != 'ResetKey'):
            conflicts.append( { 'page' : 'Preferences Dialog', 'ctrl' : 'Reset Key' } )

        return conflicts

    # check all buttons for conflicts.
    def CheckAllConflicts(self):
        for page in self.Pages:
            for _, ctrl in page.Ctrls.items():
                if isinstance(ctrl, bcKeyButton):
                    if not ctrl.IsThisEnabled(): continue
                    ctrl.CheckConflicts()

    def SetModified(self, _ = None):
        self.Parent.SetTitle(f"BindControl: {self.ProfileName()} (*)") # pyright: ignore
        self.Data.SetModified()

    def ClearModified(self, _ = None):
        self.Parent.SetTitle(f"BindControl: {self.ProfileName()}") # pyright: ignore
        self.Data.ClearModified()

    def IsModified(self): return self.Data.Modified

    ###################
    # Profile Save/Load
    def SaveAsDefault(self, prompt = True):
        if prompt:
            result = wx.MessageBox("This will set the current profile to be used as a template when making a new profile.  Continue?", "Save As Default", wx.YES_NO)
            if result == wx.NO: return

        try:
            self.Data.doSaveAsDefault()
        except Exception as e:
            # Let us know if it did
            wx.LogError(f"Failed to write default profile: {e}")

    def SaveToFile(self):
        config = wx.ConfigBase.Get()
        try:
            ProfilePath(config).mkdir( parents = True, exist_ok = True )
        except Exception as e:
            wx.LogError(f"Can't make Profile path {ProfilePath(config)} - {e}.  Aborting Save.")
            return

        with wx.FileDialog(self, "Save Profile file",
                wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(ProfilePath(config)),
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
            # TODO move this logic down into Models/ProfileData
            self.Data.Filepath = Path(pathname)
            self.Data['ProfileBindsDir'] = self.Data.GenerateBindsDirectoryName()
            if not self.Data['ProfileBindsDir']:
                # This happens if GenerateBindsDirectoryName can't come up with something sane
                self.Parent.OnProfDirButton() # pyright: ignore

            # save the new file
            self.doSaveToFile()

            # make sure we're all set up as whatever we just saved as
            mainwindow = wx.App.Get().Main
            newprofile = Profile.doLoadFromFile(mainwindow, self.Data.Filepath)
            mainwindow.InsertProfile(newprofile)

    def doSaveToFile(self):
        result = self.Data.doSaveToFile()
        self.SetTitle()
        wx.LogMessage(f"Wrote profile {self.Data.Filepath}")
        return result

    def buildUIFromData(self):
        self.SetTitle()

        self.MassageData()
        data = self.Data

        # we store the ProfileBindsDir outside of the sections
        if data and data.get('ProfileBindsDir', None):
            self.ProfileBindsDir = data['ProfileBindsDir']

        for pagename in ['General', 'Gameplay', 'MovementPowers', 'InspirationPopper', 'Mastermind']:
            page = getattr(self, pagename)
            if data and pagename in data:
                for controlname in page.Ctrls:
                    value = None
                    if controlname in data[pagename]:
                        value = data[pagename].get(controlname, None)
                    # if we don't have a given control in the load data, skip it completely --
                    # it should already have the default value from Init
                    else: continue

                    page.SetState(controlname, value)

            page.SynchronizeUI()

            # Do this after SynchronizeUI for General because SynchronizeUI has blown away our powerset
            # picks when we re-fill those pickers from the archetype.
            if data and pagename == 'General':

                # Re-fill Primary and Secondary pickers, honoring old numeric indices if needed
                prim = data['General'].get('Primary', None)
                if isinstance(prim, str):
                    page.Ctrls['Primary'].SetStringSelection(prim)
                else:
                    page.Ctrls['Primary'].SetSelection(prim)

                seco = data['General'].get('Secondary', None)
                if isinstance(seco, str):
                    page.Ctrls['Secondary'].SetStringSelection(seco)
                else:
                    page.Ctrls['Secondary'].SetSelection(seco)

                epic = data['General'].get('Epic', None)
                if isinstance(epic, str):
                    page.Ctrls['Epic'].SetStringSelection(epic)
                else:
                    page.Ctrls['Epic'].SetSelection(epic)

                # And while we're in "General" make sure the "Server" picker is set right
                page.ServerPicker.SetStringSelection(self.Server())

            page.Layout()

        cbpage = getattr(self, "CustomBinds")
        if data and cbpage:
            cbpage.scrolledPanel.DestroyChildren()
            cbpage.Ctrls = {}
            cbpage.Panes = []
            for custombind in data['CustomBinds']:
                if not custombind: continue

                # TODO - move this logic into the CustomBinds page class
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
                else:
                    wx.LogError(f'Tried to create a custom bind with unknown type "{custombind['Type']}" - probably a bug!')

                if bindpane:
                    cbpage.AddBindToPage(bindpane = bindpane)


        # Finally, after loading all this stuff, THEN add the binds that update the ProfileData
        for pagename in ['General', 'Gameplay', 'MovementPowers', 'InspirationPopper', 'Mastermind']:
            page = getattr(self, pagename)
            for evt in [
                wx.EVT_CHECKBOX, wx.EVT_BUTTON, wx.EVT_CHOICE, wx.EVT_COMBOBOX, wx.EVT_TEXT, wx.EVT_SPINCTRL,
                wx.EVT_DIRPICKER_CHANGED, wx.EVT_COLOURPICKER_CHANGED, wx.EVT_MENU, wx.EVT_RADIOBUTTON,
                wx.EVT_SLIDER, EVT_KEY_CHANGED, EVT_POWER_CHANGED, EVT_POWERBINDER_CHANGED
            ]:

                page.Bind(evt, partial(self.OnCommandEvent, pagename = pagename))

    def OnCommandEvent(self, evt, pagename):
        evt.Skip()
        page = getattr(self, pagename)
        control = getattr(evt, 'control', evt.GetEventObject())
        if ctlname := next((name for name,c in page.Ctrls.items() if control == c), None):
            # TODO:  "unless (some way to opt things out of this), then..."
            self.UpdateData(pagename, ctlname, page.GetState(ctlname))
            self.SetModified()
            self.CheckAllConflicts()

    def UpdateData(self, *args):
        self.Data.UpdateData(*args)

    # This is for mashing old legacy profiles into the current state of affairs.
    # Each step in here might eventually get deprecated but maybe not, there's
    # little downside to doing all of this forever.
    def MassageData(self):

        # load old Profiles pre-rename of "Movement Powers" tab
        if self.Data and 'SoD' in self.Data:
            self.Data['MovementPowers'] = self.Data['SoD']
            self.SetModified()

        # This option got renamed for better clarity
        if self.Data['MovementPowers']['DefaultMode'] == 'No SoD':
            self.Data['MovementPowers']['DefaultMode'] = 'No Default SoD'

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
            wx.LogError(f"Can't make binds directory {self.BindsDir()}: {e}")
            wx.MessageBox(f"Can't make binds directory {self.BindsDir()}: {e}")
            return

        otherProfile = None
        try:
            otherProfile = self.BindsDirNotMine()
        except Exception:
            wx.LogError("Something went wrong trying to check the ProfileIDFile: {e}")
            wx.MessageBox("Something went wrong trying to check the ProfileIDFile: {e}")
            return

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

        with WriteDoneDialog(self, msg = msg) as dlg:
            dlg.Show()
            dlg.Raise()
            dlg.ShowModal()
            if errors:
                for err in errors:
                    wx.LogError(err)
                wx.App.Get().Main.Logger.LogWindow.Show()

        # clear out our state
        self.Data.BindFiles = {}
        self.BindFiles = {}

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
        super().__init__(parent, title = "Bindfiles Written")

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
        super().__init__(parent, title = "Bindfiles Deleted")

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
