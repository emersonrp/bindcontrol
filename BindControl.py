#!/usr/bin/env python3
import sys
import wx
import re
import os
import platform
from pathlib import Path
import webbrowser

import wx.lib.mixins.inspection
import wx.adv
from bcLogging import bcLogging
from bcVersion import current_version
from Icon import GetIcon
from Profile import Profile
from UI.BindDirsWindow import BindDirsWindow
from UI.PrefsDialog import PrefsDialog
from Help import ShowHelpWindow
from UI.ControlGroup import cgTextCtrl, cgButton
from Util.DefaultProfile import DefaultProfile
import Util.Paths
import Util.BuildFiles

MIN_PYTHON = (3, 13)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python {}.{} or later is required.\n".format(*MIN_PYTHON))

MIN_WX = (4, 2, 2)
if wx.VERSION < MIN_WX:
    sys.exit("wxPython {}.{}.{} or later is required.\n".format(*MIN_WX))

###################
# Main Window Class
###################
class Main(wx.Frame):

    def __init__(self, guiLogging = True):
        super().__init__(None, title = "BindControl")

        self.Profile = None
        self.StartupPanel = None
        self.Logger : bcLogging|None = None

        self.about_info = None

        stdpaths = wx.StandardPaths.Get()
        config = wx.ConfigBase.Get()
        # Check each config bit for existence and set to default if no
        if not config.Exists('GamePath'):
            if platform.system() == 'Windows':
                gamepath = "C:\\Games\\Homecoming\\"
            else:
                gamepath = str(Path.home() / '.wine' / 'drive_c' / 'Games' / 'Homecoming')
            config.Write('GamePath', gamepath)
        if not config.Exists('GameLang'): config.Write('GameLang', 'English')
        if not config.Exists('BindPath'):
            if platform.system() == 'Windows':
                bindpath = "C:\\coh\\"
            else:
                bindpath = str(Path.home() / '.wine' / 'drive_c' / 'coh')
            config.Write('BindPath', bindpath)
        if not config.Exists('GameBindPath'):
            if platform.system() != 'Windows':
                config.Write('GameBindPath', "c:\\coh\\")
        if not config.Exists('ResetKey')            : config.Write('ResetKey', 'CTRL+R')
        if not config.Exists('UseSplitModKeys')     : config.WriteBool('UseSplitModKeys', False)
        if not config.Exists('FlushAllBinds')       : config.WriteBool('FlushAllBinds', True)
        if not config.Exists('ProfilePath')         : config.Write('ProfilePath', str(Path(stdpaths.GetDocumentsDir()) / "bindcontrol"))
        if not config.Exists('StartWithLastProfile'): config.WriteBool('StartWithLastProfile', True)
        if not config.Exists('SaveSizeAndPosition') : config.WriteBool('SaveSizeAndPosition', True)
        if not config.Exists('VerboseBLF')          : config.WriteBool('VerboseBLF', False)
        if not config.Exists('CrashOnBindError')    : config.WriteBool('CrashOnBindError', False)
        if not config.Exists('ShowInspector')       : config.WriteBool('ShowInspector', False)
        if not config.Exists('ShowDebugMessages')   : config.WriteBool('ShowDebugMessages', False)
        if not config.Exists('WinH')                : config.WriteInt('WinH', 1000)
        if not config.Exists('WinW')                : config.WriteInt('WinW', 1000)
        if not config.Exists('DefaultProfile')      : config.Write('DefaultProfile', DefaultProfile)

        # migrate old "start with" preference.  Maybe remove this someday
        if config.Exists('StartWith'):
            config.WriteBool('StartWithLastProfile', config.Read('StartWith') == "Last Profile")
            config.DeleteEntry('StartWith')

        config.Flush()

        # set up the custom logger with the infobar
        if guiLogging:
            self.Logger = bcLogging(self)

        if config.ReadBool('ShowDebugMessage'):
            wx.Log.SetLogLevel(wx.LOG_Debug)
        else:
            wx.Log.SetLogLevel(wx.LOG_Status)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)

        # "Profile" Menu
        ProfMenu = wx.Menu()

        Profile_new         = ProfMenu.Append(wx.ID_NEW, "&New Profile\tCTRL-N", "Create a new profile")
        Profile_load        = ProfMenu.Append(wx.ID_OPEN, "&Load Profile...\tCTRL-L", "Load an existing profile")
        self.Profile_import = ProfMenu.Append(wx.ID_ADD,  "&Import Saved Build...\tCTRL-I", "Import a build file saved from City of Heroes")
        self.Profile_save   = ProfMenu.Append(wx.ID_SAVE, "&Save Profile\tCTRL-S", "Save the current profile")
        self.Profile_saveas = ProfMenu.Append(wx.ID_SAVEAS, "Save Profile As...", "Save the current profile under a new filename")
        self.Profile_close  = ProfMenu.Append(wx.ID_CLOSE, "Close Profile", "Close the current profile")
        ProfMenu.AppendSeparator()
        self.Profile_savedefault = ProfMenu.Append(wx.ID_ANY, "Save Profile As Default", "Save the current profile as the default for new profiles")
        ProfMenu.AppendSeparator()
        Profile_preferences = ProfMenu.Append(wx.ID_PREFERENCES, "&Preferences", "Configure BindControl")
        Profile_exit  = ProfMenu.Append(wx.ID_EXIT)

        # "Help" Menu
        HelpMenu = wx.Menu()

        Help_manual   = HelpMenu.Append(wx.ID_ANY , "Manual"           , "User's Manual")
        Help_guide    = HelpMenu.Append(wx.ID_ANY , "Getting Started"  , "Getting Started Guide on the BindControl wiki")
        Help_files    = HelpMenu.Append(wx.ID_ANY , "Output Files"     , "About BindControl's Output Files")
        Help_bindDirs = HelpMenu.Append(wx.ID_ANY , "Bind Directories" , "Location of each Profile's bind files")
        Help_license  = HelpMenu.Append(wx.ID_ANY , "License Info"     , "")
        Help_bugs     = HelpMenu.Append(wx.ID_ANY , "Reporting Bugs"   , "How To Report Bugs In BindControl")
        Help_about    = HelpMenu.Append(wx.ID_ABOUT)

        LogMenu = wx.Menu()

        Log_window = LogMenu.Append(wx.ID_ANY, "Log Window", "Show the log window")

        # cram the separate menus into a menubar
        MenuBar = wx.MenuBar()
        MenuBar.Append(ProfMenu, 'Profile')
        MenuBar.Append(HelpMenu, 'Help')
        MenuBar.Append(LogMenu, 'Log')

        # glue the menubar into the main window
        self.SetMenuBar(MenuBar)

        # MENUBAR EVENTS
        self.Bind(wx.EVT_MENU , self.OnProfileNew          , Profile_new)
        self.Bind(wx.EVT_MENU , self.OnProfileLoad         , Profile_load)
        self.Bind(wx.EVT_MENU , self.OnProfileImport       , self.Profile_import)
        self.Bind(wx.EVT_MENU , self.OnProfileSave         , self.Profile_save)
        self.Bind(wx.EVT_MENU , self.OnProfileSaveAs       , self.Profile_saveas)
        self.Bind(wx.EVT_MENU , self.OnProfileSaveDefault  , self.Profile_savedefault)
        self.Bind(wx.EVT_MENU , self.OnProfileClose        , self.Profile_close)
        self.Bind(wx.EVT_MENU , self.OnMenuPrefsDialog     , Profile_preferences)
        self.Bind(wx.EVT_MENU , self.OnMenuExitApplication , Profile_exit)

        self.Bind(wx.EVT_MENU, self.OnHelpManual, Help_manual)
        self.Bind(wx.EVT_MENU, self.OnHelpGettingStarted, Help_guide)
        self.Bind(wx.EVT_MENU, self.OnHelpFiles, Help_files)
        self.Bind(wx.EVT_MENU, self.OnHelpBindDirs, Help_bindDirs)
        self.Bind(wx.EVT_MENU, self.OnHelpLicense, Help_license)
        self.Bind(wx.EVT_MENU, self.OnHelpBugs, Help_bugs)
        self.Bind(wx.EVT_MENU, self.OnMenuAboutBox, Help_about)

        self.Bind(wx.EVT_MENU, self.OnMenuLogWindow, Log_window)

        AppIcon = wx.IconBundle()
        base_path = Util.Paths.GetRootDirPath()
        filename = base_path / 'icons' / 'BindControl.ico'
        AppIcon.AddIcon(f"{filename}", wx.BITMAP_TYPE_ANY)
        self.SetIcons(AppIcon)

        # Infobar for showing errors and other messages
        if guiLogging and self.Logger:
            self.Sizer.Add(self.Logger.InfoBar, 0, wx.EXPAND)

        # Bottom Buttons
        # BUTTONS
        self.BottomButtonPanel = wx.Panel(self)
        self.ProfDirButton = cgButton(self.BottomButtonPanel, -1, "Set Binds Directory")
        self.ProfDirButton.SetToolTip("Configure the directory where this Profile will write bindfiles")
        self.ProfDirButton.DefaultToolTip = "Configure the directory where this Profile will write bindfiles"
        self.WriteButton = wx.Button(self.BottomButtonPanel, -1, "Write Binds")
        self.WriteButton.SetToolTip("Write out the bindfiles to the configured binds directory")
        self.DeleteButton = wx.Button(self.BottomButtonPanel, -1, "Delete All Binds")
        self.DeleteButton.SetToolTip("Delete all BindControl-managed files in the configured binds directory")
        BottomButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BottomButtonPanel.SetSizer(BottomButtonSizer)
        BottomButtonSizer.Add(self.ProfDirButton, 0, wx.EXPAND)
        BottomButtonSizer.Add(self.WriteButton, 1, wx.EXPAND)
        BottomButtonSizer.Add(self.DeleteButton, 0, wx.EXPAND)
        self.ProfDirButton.Bind(wx.EVT_BUTTON, self.OnProfDirButton)
        self.WriteButton  .Bind(wx.EVT_BUTTON, self.OnWriteBindsButton)
        self.DeleteButton .Bind(wx.EVT_BUTTON, self.OnDeleteBindsButton)

        self.Sizer.Add(self.BottomButtonPanel,  0, wx.EXPAND | wx.ALL, 10)

        # Do not SetSizerAndFit() - Fit() is poison
        self.SetSizer(self.Sizer)

        self.Bind(wx.EVT_CLOSE, self.OnWindowClosing)

    def SetupProfile(self, input_profile = None):

        config = wx.ConfigBase.Get()

        filename = None
        if input_profile:
            filename = input_profile
        elif (config.Read('StartWith') == 'Last Profile' or config.ReadBool('StartWithLastProfile')):
            filename = config.Read('LastProfile')

        if filename:
            try:
                profile = Profile(self, filename)
                profile.buildUIFromData()
                self.Profile = profile
                self.Sizer.Insert(0, self.Profile, 1, wx.EXPAND)
                self.CheckProfDirButtonErrors()
            except Exception:
                if self.Profile:
                    self.Profile.DestroyLater()
                self.Profile = None
                self.StartupPanel = self.MakeStartupPanel()
                self.Sizer.Insert(0, self.StartupPanel, 1, wx.EXPAND)

        # otherwise show the two big buttons
        else:
            self.StartupPanel = self.MakeStartupPanel()
            self.Sizer.Insert(0, self.StartupPanel, 1, wx.EXPAND)

        (width, height) = (1100, 800)
        if config.ReadBool('SaveSizeAndPosition') and config.HasEntry('WinH') and config.HasEntry('WinW'):
            height = config.ReadInt('WinH')
            width  = config.ReadInt('WinW')
        elif self.Profile:
            height = self.Profile.GetBestSize().height
            width  = self.Profile.GetBestSize().width + 24 # account for Profile's padding

        if width and height:
            self.SetSize(wx.Size(width, height))

        if config.ReadBool('SaveSizeAndPosition') and config.HasEntry('WinX') and config.HasEntry('WinY'):
            self.SetPosition(wx.Point((config.ReadInt('WinX'), config.ReadInt('WinY'))))

        self.BindDirsWindow = None

        self.SetupProfileUI()

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

    # This is the two-button "start new profile" vs "load existing profile" panel
    def MakeStartupPanel(self) -> wx.Panel:
        StartupPanel = wx.Panel(self)

        StartupSizer = wx.BoxSizer(wx.VERTICAL)

        ButtonSizer = wx.GridSizer(3, 10, 10)
        newButton  = wx.Button(StartupPanel, -1, "Start New Profile")
        newButton.SetBitmap(GetIcon('UI', 'new_profile'))
        newButton.SetBitmapPosition(wx.TOP)
        newButton.SetToolTip('Start a brand new profile from scratch')
        loadButton = wx.Button(StartupPanel, -1, "Load Existing Profile")
        loadButton.SetBitmap(GetIcon('UI', 'load_profile'))
        loadButton.SetBitmapPosition(wx.TOP)
        loadButton.SetToolTip('Load an existing BindControl Profile file')
        importButton = wx.Button(StartupPanel, -1, "Import Build File")
        importButton.SetBitmap(GetIcon('UI', 'import_build'))
        importButton.SetBitmapPosition(wx.TOP)
        importButton.SetToolTip('Import a build file exported from City of Heroes')
        ButtonSizer.Add(newButton, 1, wx.EXPAND)
        ButtonSizer.Add(loadButton, 1, wx.EXPAND)
        ButtonSizer.Add(importButton, 1, wx.EXPAND)

        newButton.Bind(wx.EVT_BUTTON, self.OnProfileNew)
        loadButton.Bind(wx.EVT_BUTTON, self.OnProfileLoad)
        importButton.Bind(wx.EVT_BUTTON, self.OnProfileImport)

        GettingStartedButton = wx.Button(StartupPanel, label = "Getting Started With BindControl")
        GettingStartedButton.Bind(wx.EVT_BUTTON, self.OnHelpGettingStarted)

        StartupSizer.AddStretchSpacer(1)
        StartupSizer.Add(ButtonSizer, 0, wx.ALIGN_CENTER)
        StartupSizer.Add(GettingStartedButton, 0, wx.ALIGN_CENTER|wx.TOP, 40)
        StartupSizer.AddStretchSpacer(1)

        StartupPanel.SetSizer(StartupSizer)
        StartupPanel.Layout()

        return StartupPanel

    def SetupProfileUI(self) -> None:
        enable = self.Profile is not None
        self.Profile_save.Enable(enable)
        self.Profile_saveas.Enable(enable)
        self.Profile_savedefault.Enable(enable)
        self.ProfDirButton.Enable(enable)
        # TODO - do smarter things with enabling the write and delete buttons
        self.WriteButton.Enable(enable)
        self.DeleteButton.Enable(enable)

    def OnPageChanged(self, evt) -> None:
        if self.Profile:
            tabnumber = evt.GetSelection()
            tabname = self.Profile.GetPageText(tabnumber)
            if tabname == "Popmenu Editor":
                self.BottomButtonPanel.Hide()
                if self.Profile:
                    self.Profile.PopmenuEditor.LoadMenusIfNeeded()
                    self.Profile.PopmenuEditor.SynchronizeUI()
            else:
                self.BottomButtonPanel.Show(True)
            self.Layout()

    def OnProfileNew(self, _ = None) -> None:
        if self.CheckIfProfileNeedsSaving() == wx.CANCEL: return
        # loop eternally until we get a name we like
        while True:
            with wx.TextEntryDialog(self, message = 'Enter name for new profile, for instance, the name of a character:', caption = "New Profile") as dlg:
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    newname = dlg.GetValue()
                    if not newname:
                        continue
                    checkprofile = Path(wx.ConfigBase.Get().Read('ProfilePath'))/ f"{newname}.bcp"
                    if checkprofile.exists():
                        wx.MessageBox(f"A profile called {newname} already exists.  Please select another name.")
                        continue
                    break
                else:
                    return result

        self.Freeze()
        try:
            with wx.WindowDisabler():
                _ = wx.BusyInfo(wx.BusyInfoFlags().Parent(self).Text(f'Creating New Profile {newname}...'))
                wx.GetApp().Yield()

                self.Sizer.Remove(0)

                if self.Profile: self.Profile.Destroy()

                # destroy the Startup Panel if it's there.  This is only needed on Windows dunno why.
                if self.StartupPanel: self.StartupPanel.Destroy()

                self.Profile = Profile(self, newname = newname)
                self.Profile.buildUIFromData()
                self.Profile.SetModified()
                wx.LogMessage(f'Created New Profile "{newname}".')

                self.Sizer.Insert(0, self.Profile, 1, wx.EXPAND)

        except Exception as e:
            wx.LogError(f"Something broke in new profile: {e}.  This is a bug.")
        finally:
            self.SetupProfileUI()
            self.CheckProfDirButtonErrors()
            self.Layout()
            self.Thaw()

    def OnProfileLoad(self, _) -> None:
        if self.CheckIfProfileNeedsSaving() == wx.CANCEL: return

        # Try to load;  if the user hits "cancel" or the load fails, go back to where we were
        if newProfile:= Profile.LoadFromFile(self):
            self.InsertProfile(newProfile)

    # we use this in the Binds Directory Window also
    def InsertProfile(self, newProfile) -> bool:
        try:
            self.Freeze()

            # OK, we're either at the startup panel or we have an existing profile.  Either way, remove it:
            self.Sizer.Remove(0)

            # delete any existing Profile and all its subwidgets and geegaws
            if self.Profile: self.Profile.DestroyLater()

            # destroy the Startup Panel if it's there.  This is only needed on Windows dunno why.
            if self.StartupPanel: self.StartupPanel.DestroyLater()

            # and set up our new profile as the current one
            self.Profile = newProfile
            self.Sizer.Insert(0, self.Profile, 1, wx.EXPAND)
            self.Layout()

        except Exception as e:
            wx.LogError(f"Something broke while setting up profile load: {e}")
            return False

        finally:
            if self.IsFrozen(): self.Thaw()

        # OK, we made it, set up the UI bits etc.
        self.SetupProfileUI()
        self.CheckProfDirButtonErrors()
        wx.ConfigBase.Get().Write('LastProfile', str(newProfile.Filepath()))
        wx.ConfigBase.Get().Flush()
        return True

    def OnProfileImport(self, _) -> bool:
        if self.CheckIfProfileNeedsSaving() == wx.CANCEL: return False

        pathname = ''
        config = wx.ConfigBase.Get()
        with wx.FileDialog(self, "Import build file",
                wildcard   = "Text Files (*.txt)|*.txt|All Files (*.*)|*.*",
                defaultDir = config.Read('GamePath'),
                style      = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogMessage("User canceled importing build file")
                return False # the user changed their mind

            pathname = fileDialog.GetPath()

        if pathname:
            buildfile = Path(pathname)

            if profiledata := Util.BuildFiles.ParseBuildFile(buildfile):
                generaldata = {'General' : profiledata}
                if newprofile := Profile(self, newname = profiledata['Name'], profiledata = generaldata):
                    newprofile.buildUIFromData()
                    self.InsertProfile(newprofile)
                    newprofile.SetModified()
            else:
                wx.LogError('Build file was empty or contained errors')
                return False

        return True

    def OnProfileSave(self, _) -> None:
        if not self.Profile: return
        self.Profile.doSaveToFile()

    def OnProfileSaveAs(self, _) -> None:
        if not self.Profile: return
        self.Profile.SaveToFile()

    def OnProfileSaveDefault(self, _) -> None:
        if not self.Profile: return
        self.Profile.SaveAsDefault()

    def OnProfileClose(self, _) -> None:
        if not self.Profile: return
        if self.CheckIfProfileNeedsSaving() == wx.CANCEL: return
        self.Sizer.Remove(0)
        if self.Profile:
            self.Profile.DestroyLater()
            self.Profile = None
            wx.ConfigBase.Get().Write('LastProfile', '')
            wx.ConfigBase.Get().Flush()
        self.StartupPanel = self.MakeStartupPanel()
        self.Sizer.Insert(0, self.StartupPanel, 1, wx.EXPAND)
        self.SetTitle('BindControl')
        self.SetupProfileUI()
        self.Layout()

    def OnProfDirButton(self, _ = None) -> None:
        if not self.Profile: return # should try not to get here in the first place
        ProfDirDialog = wx.Dialog(self, -1, "Set Binds Directory")

        sizer = wx.BoxSizer(wx.VERTICAL)
        ProfDirDialog.SetSizer(sizer)

        sizer.Add(wx.StaticText(ProfDirDialog, -1, "Select the directory where this profile will write its bindfiles:"), 1, wx.EXPAND|wx.ALL, 10)

        config = wx.ConfigBase.Get()
        bindpath = config.Read('BindPath')
        separator = "\\" if platform.system() == "Windows" else "/"
        if bindpath[-1:] == separator: separator = ''

        dirSizer = wx.BoxSizer(wx.HORIZONTAL)
        dirSizer.Add(wx.StaticText(ProfDirDialog, -1,
                    f"{bindpath}{separator}"), 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
        PathText = cgTextCtrl(ProfDirDialog, -1)
        dirSizer.Add(PathText, 1, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        PathText.Bind(wx.EVT_TEXT, self.OnPathTextChanged)

        sizer.Add(dirSizer, 1, wx.EXPAND)

        sizer.Add(wx.StaticText(ProfDirDialog, -1, "Changing this value will automatically save the Profile,\nincluding any other changes you have made."), 1, wx.EXPAND|wx.ALL, 10)

        buttonsizer = ProfDirDialog.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL)

        sizer.Add(buttonsizer, 1, wx.EXPAND|wx.ALL, 10)

        ProfDirDialog.Layout()

        PathText.ClearErrors() # whyyyy?

        with ProfDirDialog as dlg:
            PathText.SetValue(self.Profile.ProfileBindsDir) # do this here to trigger wx.EVT_TEXT
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                newvalue = PathText.GetValue()
                # call us again if we tried to OK an error state
                if PathText.HasErrors(): return self.OnProfDirButton()
                # if we changed the directory, offer to delete the old one.

                otherprofile = Util.Paths.CheckProfileForBindsDir(config, self.Profile.ProfileBindsDir)
                if (
                    # we changed it to a new value:
                    self.Profile.ProfileBindsDir and (newvalue != self.Profile.ProfileBindsDir)
                        and
                    # the old one isn't owned by another profile:
                    ((not otherprofile) or (otherprofile and (otherprofile == self.Profile.ProfileName())))
                ):
                    answer = wx.MessageBox(
                            f'Binds directory changed.  Delete all binds in old binds directory?\n{self.Profile.BindsDir()}',
                            'Binds directory Changed',wx.YES_NO, self
                    )
                    if answer == wx.YES:
                        self.Profile.DeleteBindFiles()
                self.Profile.ProfileBindsDir = newvalue
                self.Profile.doSaveToFile()

        # need this out here in case we cancelled on a previously-blank one.
        # This is very very unlikely to happen and awful if it does.
        # TODO: yes later on I see that this is indeed awful.  Fix it.
        #
        # TODO-ish:  if they erase an existing valid one or otherwise cause an
        # error, and then hit "cancel" this gets triggered, which is not
        # perfect - this logic needs a little smartening.
        if PathText.HasErrors(): return self.OnProfDirButton()

        self.CheckProfDirButtonErrors()

    def CheckIfProfileNeedsSaving(self) -> int:
        result = wx.OK
        if self.Profile:
            if self.Profile.IsModified():
                result = wx.MessageBox(f"Profile {self.Profile.ProfileName()} not saved, save now?", "Profile modified", wx.YES_NO|wx.CANCEL)
                if result == wx.YES:
                    self.Profile.doSaveToFile()
            if self.Profile.PopmenuEditor.CheckForModifiedMenus():
                result = wx.MessageBox("Some popmenus contain unsaved changes, return to editor?", "Popmenus modified", wx.YES_NO)
                if result == wx.YES:
                    result = wx.CANCEL
                    peidx = self.Profile.FindPage(self.Profile.PopmenuEditor)
                    self.Profile.SetSelection(peidx)
        return result

    def CheckProfDirButtonErrors(self) -> None:
        config = wx.ConfigBase.Get()
        if not self.Profile: return
        if self.Profile.ProfileBindsDir:
            self.ProfDirButton.RemoveError('undef')
        else:
            self.ProfDirButton.AddError('undef', 'Your binds directory is unset.  Binds cannot be written.')

        if len(self.Profile.ProfileBindsDir) <= 8:
            self.ProfDirButton.RemoveWarning('toolong')
        else:
            self.ProfDirButton.AddWarning('toolong', 'Your binds directory name is rather long.  This is not an error but can lead to some binds being too long for the game to use.')

        otherprofile = Util.Paths.CheckProfileForBindsDir(config, self.Profile.ProfileBindsDir)
        if otherprofile and (otherprofile != self.Profile.ProfileName()):
            self.ProfDirButton.AddWarning('owned', f'The binds directory you have chosen is marked as owned by the profile "{otherprofile}."  This is not an error, but be sure this is what you want to do.')
        else:
            self.ProfDirButton.RemoveWarning('owned')

        self.DeleteButton.Enable(not self.ProfDirButton.HasErrors())
        self.WriteButton.Enable(not self.ProfDirButton.HasErrors())

    def OnPathTextChanged(self, evt) -> None:
        textctrl = evt.EventObject
        value = textctrl.GetValue()

        if not value:
            textctrl.AddError('undef', 'You must specify a bindfile directory name.')
        else:
            textctrl.RemoveError('undef')

        if re.search(r'[^A-Za-z0-9_]', value):
            textctrl.AddError('unicode', 'The binds directory must contain only A-Z, a-z, 0-9, and _ characters.')
        else:
            textctrl.RemoveError('unicode')

        if re.search(r'\s', value):
            textctrl.AddError('spaces', 'The binds directory cannot contain spaces.')
        else:
            textctrl.RemoveError('spaces')

        if platform.system() == 'Windows':
            if os.path.isreserved(value): # pyright: ignore
                textctrl.AddError('reserved', 'The name you have selected is a reserved filename in Windows.  Please select another.')
            else:
                textctrl.RemoveError('reserved')

        if value: # don't do this check if it's blank
            exists = None
            # look at the existing bindsdirs and see if we match
            for bindsdir in Util.Paths.GetAllProfileBindsDirs(config):
                # check case-insensitive because Windows
                if bindsdir.lower() == value.lower():
                    # but stash it away as the case-sensitive version because Linux
                    exists = bindsdir
                    break
            if exists and self.Profile:
                existingProfile = Util.Paths.CheckProfileForBindsDir(config, exists)
                if existingProfile != self.Profile.ProfileName():
                    existingProfileWarning = f', and is managed by the profile {existingProfile}' if existingProfile else ''
                    textctrl.AddWarning('exists', f'The directory you have selected already exists{existingProfileWarning}.  This is not an error, but be sure this is where you want to save your binds.')
            else:
                textctrl.RemoveWarning('exists')

    def OnWriteBindsButton(self, _) -> None:
        if not self.Profile: return
        self.Profile.WriteBindFiles()

    def OnDeleteBindsButton(self, _) -> None:
        if not self.Profile: return
        self.Profile.DeleteBindFiles()

    def OnMenuPrefsDialog(self, _ = None) -> None:
        with PrefsDialog(self) as dlg:
            dlg.ShowAndUpdatePrefs()

    def OnMenuAboutBox(self, _) -> None:
        from datetime import datetime
        this_year = datetime.now().year
        if self.about_info is None:
            info = wx.adv.AboutDialogInfo()
            info.AddDeveloper('R Pickett (emerson@hayseed.net)')
            info.SetName('BindControl')
            info.SetVersion(current_version())
            info.SetDescription(
                "BindControl can help you set up custom keybinds and popmenus in City of Heroes.\n\n"

                "Based on CityBinder 0.76, Copyright \u00A9 2005-2006 Jeff Sheets,\nand CityBinder for Homecoming 0.2, Copyright \u00A9 2021-2023 tailcoat\n\n"

                "Speed-On-Demand binds originally created by Gnarley's Speed On Demand Binds,\nupdated for Homecoming by emerson.  Advanced Teleport Binds originally by\nDrLetharga, updated for Homecoming by emerson.\n\n"

                "Mastermind binds by Sandolphan in CoV beta, updated by Konoko and emerson.\n\n"

                "Inspiration Popper design adapted from CityBinder for Homecoming by Tailcoat."
            )
            info.SetCopyright(f'\u00A9 2010-{this_year} R Pickett <emerson@hayseed.net>')
            info.SetWebSite('https://github.com/emersonrp/bindcontrol')
            self.about_info = info

        wx.adv.AboutBox(self.about_info)

    def OnMenuLogWindow(self, _) -> None:
        if self.Logger:
            self.Logger.LogWindow.Show()

    def OnMenuExitApplication(self, _) -> None:
        self.Close()

    def OnHelpManual(self, _) -> None:
        ShowHelpWindow(self, 'Manual.html')

    def OnHelpGettingStarted(self, _) -> None:
        webbrowser.open('https://github.com/emersonrp/bindcontrol/wiki/Getting-Started-With-BindControl')

    def OnHelpLicense(self, _) -> None:
        ShowHelpWindow(self, 'LICENSE.html')

    def OnHelpBugs(self, _) -> None:
        ShowHelpWindow(self, 'ReportingBugs.html')

    def OnHelpFiles(self, _) -> None:
        ShowHelpWindow(self, 'OutputFiles.html')

    # TODO - make just one window instead of a new one every time the menu item is picked
    def OnHelpBindDirs(self, _) -> None:
        window = BindDirsWindow(self, title = "Bind Directories", style = wx.TINY_CAPTION|wx.CLOSE_BOX|wx.CAPTION)
        window.Show()

    def OnWindowClosing(self, evt) -> None:
        if self.CheckIfProfileNeedsSaving() == wx.CANCEL: return

        config = wx.ConfigBase.Get()
        if config.ReadBool('SaveSizeAndPosition'):
            config.WriteInt('WinX', self.GetPosition().x)
            config.WriteInt('WinY', self.GetPosition().y)
            config.WriteInt('WinH', self.GetSize().height)
            config.WriteInt('WinW', self.GetSize().width)
            config.Flush()
        evt.Skip()

class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        # Let's try to unbuffer "print" for easier debug
        # This per "Perkins"' comment on https://stackoverflow.com/questions/107705/disable-output-buffering
        import builtins
        import functools
        builtins.print = functools.partial(print, flush=True)

        self.Init()

        return True

    def Populate(self, input_profile):
        with wx.WindowDisabler():
            _ = wx.BusyInfo('Initializing BindControl...')
            wx.GetApp().Yield()

            self.Main = Main()
            self.Main.SetupProfile(input_profile = input_profile)

            # TODO bootstrapping problem, can't do this inside Profile's "__init__" because
            # Profile needs to be defined/initialized deep inside its innards.
            if self.Main.Profile:
                self.Main.Profile.CheckAllConflicts()

        self.Main.Show()

if __name__ == "__main__":

    argv = sys.argv
    if len(argv) > 2:
        print()
        print("Usage:  BindControl.py [profile_file]")
        print()
        print("profile_file is optional, and should be a *.bcp file")
        print()
        exit()

    input_profile = ''
    filename = argv[1] if len(argv) == 2 else None
    if filename:
        if re.search(r'\.bcp$', filename):
            input_profile = filename

    app = MyApp(redirect=False)

    stdpaths = wx.StandardPaths.Get()
    if platform.system() == "Linux":
        stdpaths.SetFileLayout(stdpaths.FileLayout_XDG)

    config = wx.FileConfig('bindcontrol')
    wx.ConfigBase.Set(config)

    app.Populate(input_profile)

    if config.ReadBool('ShowInspector'):
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()
