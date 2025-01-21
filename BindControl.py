#!/usr/bin/env python3
import sys, os, platform, re
from pathlib import Path
import webbrowser

import wx
import wx.lib.mixins.inspection
import wx.adv
import wx.html
from bcLogging import bcLogging
from bcVersion import current_version
from Icon import GetIcon
import Profile
from UI.BindDirsWindow import BindDirsWindow
from UI.PrefsDialog import PrefsDialog
from Help import ShowHelpWindow
from UI.ControlGroup import cgTextCtrl, cgButton

###################
# Main Window Class
###################
class Main(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title = "BindControl")

        self.Profile = None
        self.StartupPanel = None

        self.about_info = None

        # TODO - most (NOT ALL) of this code can be deleted eventually.
        if platform.system() == "Linux":
            # First connect with the old-style .bindcontrol if it's there.
            oldconfig = wx.FileConfig('bindcontrol')
            # Set up XDG.  KEEP THIS LINE even if we remove the migration code
            wx.StandardPaths.Get().SetFileLayout(wx.StandardPaths.Get().FileLayout.FileLayout_XDG)
            # Then connect to the new location
            config = wx.FileConfig('bindcontrol')
            if oldconfig.Exists('ResetKey'):
                wx.LogMessage("Migrating old-style .bindcontrol config to XDG path")
                entries = {}
                more, value, index = oldconfig.GetFirstEntry()
                while more:
                    entries[value] = oldconfig.GetEntryType(value)
                    more, value, index = oldconfig.GetNextEntry(index)

                for entry, type in entries.items():
                    if type == wx.ConfigBase.Get().EntryType.Type_String:
                        config.Write(entry, oldconfig.Read(entry))
                    elif type == wx.ConfigBase.Get().EntryType.Type_Boolean:
                        config.WriteBool(entry, oldconfig.ReadBool(entry))
                    elif type == wx.ConfigBase.Get().EntryType.Type_Integer:
                        config.WriteInt(entry, oldconfig.ReadInt(entry))
                    elif type == wx.ConfigBase.Get().EntryType.Type_Float:
                        config.WriteFloat(entry, oldconfig.ReadFloat(entry))

                config.Flush()
                oldconfig.DeleteAll()

        # OK, all that ugliness out of the way, re-open config and let's proceed.
        config = wx.FileConfig('bindcontrol')
        wx.ConfigBase.Set(config)
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
        if not config.Exists('ProfilePath')         : config.Write('ProfilePath', str(Path(wx.StandardPaths.Get().GetDocumentsDir()) / "bindcontrol"))
        if not config.Exists('StartWithLastProfile'): config.WriteBool('StartWithLastProfile', True)
        if not config.Exists('SaveSizeAndPosition') : config.WriteBool('SaveSizeAndPosition', True)
        if not config.Exists('VerboseBLF')          : config.WriteBool('VerboseBLF', False)
        if not config.Exists('CrashOnBindError')    : config.WriteBool('CrashOnBindError', False)
        if not config.Exists('ShowInspector')       : config.WriteBool('ShowInspector', False)
        if not config.Exists('ShowDebugMessages')   : config.WriteBool('ShowDebugMessages', False)
        if not config.Exists('WinH')                : config.WriteInt('WinH', 1000)
        if not config.Exists('WinW')                : config.WriteInt('WinW', 1000)

        # migrate old "start with" preference.  Maybe remove this someday
        if config.Exists('StartWith'):
            config.WriteBool('StartWithLastProfile', config.Read('StartWith') == "Last Profile")
            config.DeleteEntry('StartWith')

        config.Flush()

        # set up the custom logger with the infobar
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
        self.Profile_save   = ProfMenu.Append(wx.ID_SAVE, "&Save Profile\tCTRL-S", "Save the current profile")
        self.Profile_saveas = ProfMenu.Append(wx.ID_SAVEAS, "Save Profile As...", "Save the current profile under a new filename")
        ProfMenu.AppendSeparator()
        self.Profile_savedefault = ProfMenu.Append(wx.ID_ANY, "Save Profile As Default", "Save the current profile as the default for new profiles")
        ProfMenu.AppendSeparator()
        Profile_preferences = ProfMenu.Append(wx.ID_PREFERENCES, "&Preferences", "Configure BindControl")
        Profile_exit  = ProfMenu.Append(wx.ID_EXIT)

        # "Help" Menu
        HelpMenu = wx.Menu()

        Help_manual   = HelpMenu.Append(wx.ID_ANY,"Manual","User's Manual")
        Help_guide    = HelpMenu.Append(wx.ID_ANY,"Getting Started","Getting Started Guide on the BindControl wiki")
        Help_files    = HelpMenu.Append(wx.ID_ANY,"Files","About BindControl's Output Files")
        Help_bindDirs = HelpMenu.Append(wx.ID_ANY, "Bind Directories", "Location of each Profile's bind files")
        Help_license  = HelpMenu.Append(wx.ID_ANY,"License Info","")
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
        self.Bind(wx.EVT_MENU , self.OnProfileSave         , self.Profile_save)
        self.Bind(wx.EVT_MENU , self.OnProfileSaveAs       , self.Profile_saveas)
        self.Bind(wx.EVT_MENU , self.OnProfileSaveDefault  , self.Profile_savedefault)
        self.Bind(wx.EVT_MENU , self.OnMenuPrefsDialog     , Profile_preferences)
        self.Bind(wx.EVT_MENU , self.OnMenuExitApplication , Profile_exit)

        self.Bind(wx.EVT_MENU, self.OnHelpManual, Help_manual)
        self.Bind(wx.EVT_MENU, self.OnHelpGettingStarted, Help_guide)
        self.Bind(wx.EVT_MENU, self.OnHelpFiles, Help_files)
        self.Bind(wx.EVT_MENU, self.OnHelpBindDirs, Help_bindDirs)
        self.Bind(wx.EVT_MENU, self.OnHelpLicense, Help_license)
        self.Bind(wx.EVT_MENU, self.OnMenuAboutBox, Help_about)

        self.Bind(wx.EVT_MENU, self.OnMenuLogWindow, Log_window)

        self.AppIcon = wx.IconBundle()
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        filename = f"{base_path}/icons/BindControl.ico"
        self.AppIcon.AddIcon(filename, wx.BITMAP_TYPE_ANY)
        self.SetIcons(self.AppIcon)

        # Infobar for showing errors and other messages
        self.Sizer.Add(self.Logger.InfoBar, 0, wx.EXPAND)

        # Bottom Buttons
        # BUTTONS
        self.BottomButtonPanel = wx.Panel(self)
        self.ProfDirButton = cgButton(self.BottomButtonPanel, -1, "Set Binds Location")
        self.ProfDirButton.SetToolTip("Configure the location where this Profile will write bindfiles")
        self.ProfDirButton.DefaultToolTip = "Configure the location where this Profile will write bindfiles"
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

    def SetupProfile(self):

        config = wx.FileConfig('bindcontrol')

        # Load up the last profile if the pref says to and if it's there
        filename = config.Read('LastProfile')
        if (config.Read('StartWith') == 'Last Profile' or config.ReadBool('StartWithLastProfile')) and filename:
            self.Profile = Profile.Profile(self)
            if self.Profile.doLoadFromFile(filename):
                self.Sizer.Insert(0, self.Profile, 1, wx.EXPAND)
                self.CheckProfDirButtonErrors()
            else:
                self.Profile.Destroy()
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
            self.SetSize((width, height))

        if config.ReadBool('SaveSizeAndPosition') and config.HasEntry('WinX') and config.HasEntry('WinY'):
            self.SetPosition((config.ReadInt('WinX'), config.ReadInt('WinY')))

        self.BindDirsWindow = None

        self.SetupProfileUI()

    # This is the two-button "start new profile" vs "load existing profile" panel
    def MakeStartupPanel(self):
        StartupPanel = wx.Panel(self)

        StartupSizer = wx.BoxSizer(wx.VERTICAL)

        ButtonSizer = wx.GridSizer(2, 10, 10)
        newButton  = wx.Button(StartupPanel, -1, "Start New Profile")
        newButton.SetBitmap(GetIcon('UI/new_profile'))
        newButton.SetBitmapPosition(wx.TOP)
        loadButton = wx.Button(StartupPanel, -1, "Load Existing Profile")
        loadButton.SetBitmap(GetIcon('UI/load_profile'))
        loadButton.SetBitmapPosition(wx.TOP)
        ButtonSizer.Add(newButton, 1, wx.EXPAND)
        ButtonSizer.Add(loadButton, 1, wx.EXPAND)

        newButton.Bind(wx.EVT_BUTTON, self.OnProfileNew)
        loadButton.Bind(wx.EVT_BUTTON, self.OnProfileLoad)

        StartupSizer.AddStretchSpacer(1)
        StartupSizer.Add(ButtonSizer, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 50)
        StartupSizer.AddStretchSpacer(1)

        StartupPanel.SetSizer(StartupSizer)
        StartupPanel.Layout()

        return StartupPanel

    def SetupProfileUI(self):
        enable = self.Profile != None
        self.Profile_save.Enable(enable)
        self.Profile_saveas.Enable(enable)
        self.Profile_savedefault.Enable(enable)
        self.ProfDirButton.Enable(enable)
        # TODO - do smarter things with enabling the write and delete buttons
        self.WriteButton.Enable(enable)
        self.DeleteButton.Enable(enable)

    def OnPageChanged(self, evt):
        if evt.GetSelection() == 6:
            self.BottomButtonPanel.Hide()
            if self.Profile:
                self.Profile.PopmenuEditor.SynchronizeUI()
        else:
            self.BottomButtonPanel.Show(True)
        self.Layout()

    def OnProfileNew(self, _ = None):
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
            self.Sizer.Remove(0)

            if self.Profile: self.Profile.Destroy()

            # destroy the Startup Panel if it's there.  This is only needed on Windows dunno why.
            if self.StartupPanel: self.StartupPanel.Destroy()

            self.Profile = Profile.Profile(self)
            self.Sizer.Insert(0, self.Profile, 1, wx.EXPAND)

            self.Profile.LoadFromDefault(newname)
            wx.LogMessage(f'Created New Profile "{newname}".')

        except Exception as e:
            wx.LogError(f"Something broke in new profile: {e}.  This is a bug.")
        finally:
            self.SetupProfileUI()
            self.CheckProfDirButtonErrors()
            self.Layout()
            self.Thaw()

    def OnProfileLoad(self, _):
        if self.CheckIfProfileNeedsSaving() == wx.CANCEL: return

        newProfile = Profile.LoadFromFile(self)

        # Try to load;  if the user hits "cancel" or the load fails, go back to where we were
        if newProfile:
            self.InsertProfile(newProfile)

    # we use this in the Binds Directory Window also
    def InsertProfile(self, newProfile):
        try:
            self.Freeze()

            # OK, we're either at the startup panel or we have an existing profile.  Either way, remove it:
            self.Sizer.Remove(0)

            # delete any existing Profile and all its subwidgets and geegaws
            if self.Profile: self.Profile.Destroy()

            # destroy the Startup Panel if it's there.  This is only needed on Windows dunno why.
            if self.StartupPanel: self.StartupPanel.Destroy()

            # and set up our new profile as the current one
            self.Profile = newProfile
            self.Sizer.Insert(0, self.Profile, 1, wx.EXPAND)
            self.Layout()

        except Exception as e:
            wx.LogError(f"Something broke while setting up profile load: {e}")
            return

        finally:
            if self.IsFrozen(): self.Thaw()

        # OK, we made it, set up the UI bits etc.
        self.SetupProfileUI()
        self.CheckProfDirButtonErrors()
        wx.ConfigBase.Get().Write('LastProfile', str(newProfile.Filename))
        wx.ConfigBase.Get().Flush()

    def OnProfileSave(self, evt):
        if not self.Profile: return
        self.Profile.doSaveToFile(evt)

    def OnProfileSaveAs(self, evt):
        if not self.Profile: return
        self.Profile.SaveToFile(evt)

    def OnProfileSaveDefault(self, _):
        if not self.Profile: return
        self.Profile.SaveAsDefault()

    def OnProfDirButton(self, _ = None):
        if not self.Profile: return # should try not to get here in the first place
        ProfDirDialog = wx.Dialog(self, -1, "Set Binds Location")

        sizer = wx.BoxSizer(wx.VERTICAL)
        ProfDirDialog.SetSizer(sizer)

        sizer.Add(wx.StaticText(ProfDirDialog, -1, "Select the location where this profile will write its bindfiles:"), 1, wx.EXPAND|wx.ALL, 10)

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

                otherprofile = Profile.CheckProfileForBindsDir(self.Profile.ProfileBindsDir)
                if (
                    # we changed it to a new value:
                    self.Profile.ProfileBindsDir and (newvalue != self.Profile.ProfileBindsDir)
                        and
                    # the old one isn't owned by another profile:
                    ((not otherprofile) or (otherprofile and (otherprofile == self.Profile.Name())))
                ):
                    answer = wx.MessageBox(
                            f'Binds Location changed.  Delete all binds in old binds directory?\n{self.Profile.BindsDir()}',
                            'Binds Location Changed',wx.YES_NO, self
                    )
                    if answer == wx.YES:
                        self.Profile.DeleteBindFiles()
                self.Profile.ProfileBindsDir = newvalue
                self.Profile.doSaveToFile()

        # need this out here in case we cancelled on a previously-blank one.
        # This is very very unlikely to happen and awful if it does.
        #
        # TODO-ish:  if they erase an existing valid one or otherwise cause an
        # error, and then hit "cancel" this gets triggered, which is not
        # perfect - this logic needs a little smartening.
        if PathText.HasErrors(): return self.OnProfDirButton()

        self.CheckProfDirButtonErrors()

    def CheckIfProfileNeedsSaving(self):
        result = wx.OK
        if self.Profile:
            if self.Profile.Modified:
                result = wx.MessageBox("Profile not saved, save now?", "Profile modified", wx.YES_NO|wx.CANCEL)
                if result == wx.YES:
                    self.Profile.doSaveToFile()
            if self.Profile.PopmenuEditor.CheckForModifiedMenus():
                result = wx.MessageBox("Some popmenus contain unsaved changes, return to editor?", "Popmenus modified", wx.YES_NO)
                if result == wx.YES:
                    result = wx.CANCEL
                    self.Profile.SetSelection(6) # TODO - hardcoded "6" is ugly but meh
        return result

    def CheckProfDirButtonErrors(self):
        if not self.Profile: return
        if self.Profile.ProfileBindsDir:
            self.ProfDirButton.RemoveError('undef')
        else:
            self.ProfDirButton.AddError('undef', 'Your binds directory is unset.  Binds cannot be written.')

        if len(self.Profile.ProfileBindsDir) <= 8:
            self.ProfDirButton.RemoveWarning('toolong')
        else:
            self.ProfDirButton.AddWarning('toolong', 'Your binds directory name is rather long.  This is not an error but can lead to some binds being too long for the game to use.')

        otherprofile = Profile.CheckProfileForBindsDir(self.Profile.ProfileBindsDir)
        if otherprofile and (otherprofile != self.Profile.Name()):
            self.ProfDirButton.AddWarning('owned', f'The binds directory you have chosen is marked as owned by the profile "{otherprofile}."  This is not an error, but be sure this is what you want to do.')
        else:
            self.ProfDirButton.RemoveWarning('owned')

        self.DeleteButton.Enable(not self.ProfDirButton.HasErrors())
        self.WriteButton.Enable(not self.ProfDirButton.HasErrors())

    def OnPathTextChanged(self, evt):
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
            if os.path.isreserved(value):
                textctrl.AddError('reserved', 'The name you have selected is a reserved filename in Windows.  Please select another.')
            else:
                textctrl.RemoveError('reserved')

        if value: # don't do this check if it's blank
            exists = None
            # look at the existing bindsdirs and see if we match
            for bindsdir in Profile.GetAllProfileBindsDirs():
                # check case-insensitive because Windows
                if bindsdir.lower() == value.lower():
                    # but stash it away as the case-sensitive version because Linux
                    exists = bindsdir
                    break
            if exists and self.Profile:
                existingProfile = Profile.CheckProfileForBindsDir(exists)
                if existingProfile != self.Profile.Name():
                    existingProfileWarning = f', and is managed by the profile {existingProfile}' if existingProfile else ''
                    textctrl.AddWarning('exists', f'The directory you have selected already exists{existingProfileWarning}.  This is not an error, but be sure this is where you want to save your binds.')
            else:
                textctrl.RemoveWarning('exists')

    def OnWriteBindsButton(self, _):
        if not self.Profile: return
        self.Profile.WriteBindFiles()

    def OnDeleteBindsButton(self, _):
        if not self.Profile: return
        self.Profile.DeleteBindFiles()

    def OnMenuPrefsDialog(self, _ = None):
        with PrefsDialog(self) as dlg:
            dlg.ShowAndUpdatePrefs()

    def OnMenuAboutBox(self, _):
        from datetime import datetime
        this_year = datetime.now().year
        if self.about_info is None:
            info = wx.adv.AboutDialogInfo()
            info.AddDeveloper('R Pickett (emerson@hayseed.net)')
            info.SetName('BindControl')
            info.SetVersion(current_version())
            info.SetDescription((
                "BindControl can help you set up custom keybinds in City of Heroes/Villains, including speed-on-demand binds.\n\n"

                "Based on CityBinder 0.76, Copyright (c) 2005-2006 Jeff Sheets, and CityBinder for Homecoming 0.2, Copyright (c) 2021-2023 tailcoat\n\n"

                "Speed-On-Demand binds were originally created by Gnarley's Speed On Demand Binds Program, updated for Homecoming by emerson.  Advanced Teleport Binds originally by DrLetharga, updated for Homecoming by emerson.\n\n"

                "Mastermind binds originally by Sandolphan in CoV beta, later updated by Konoko and emerson.\n\n"

                "Inspiration Popper design adapted from CityBinder for Homecoming by Tailcoat."
            ))
            info.SetCopyright(f'(c) 2010-{this_year} R Pickett <emerson@hayseed.net>')
            info.SetWebSite('https://github.com/emersonrp/bindcontrol')
            self.about_info = info

        wx.adv.AboutBox(self.about_info)

    def OnMenuLogWindow(self, _):
        self.Logger.LogWindow.Show()

    def OnMenuExitApplication(self, _):
        self.Close()

    def OnHelpManual(self, _):
        ShowHelpWindow(self, 'Manual.html')

    def OnHelpGettingStarted(self, _):
        webbrowser.open('https://github.com/emersonrp/bindcontrol/wiki/Getting-Started-With-BindControl')

    def OnHelpLicense(self, _):
        ShowHelpWindow(self, 'LICENSE.html')

    def OnHelpFiles(self, _):
        ShowHelpWindow(self, 'OutputFiles.html')

    # TODO - make just one window instead of a new one every time the menu item is picked
    def OnHelpBindDirs(self, _):
        window = BindDirsWindow(self, title = "Bind Directories", style = wx.TINY_CAPTION|wx.CLOSE_BOX|wx.CAPTION)
        window.Show()

    def OnWindowClosing(self, evt):
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

        self.Profile = None  # needed inside Main()

        self.Init()
        with wx.WindowDisabler():
            _ = wx.BusyInfo('Initializing...')
            wx.GetApp().Yield()

            self.Main = Main(None)
            self.Main.SetupProfile()

            # TODO bootstrapping problem, can't do this inside Profile's "__init__" because
            # Profile needs to be defined/initialized deep inside its innards.
            if self.Main.Profile:
                self.Main.Profile.CheckAllConflicts()

        self.Main.Show()

        return True

if __name__ == "__main__":
    app = MyApp(redirect=False)

    config = wx.ConfigBase.Get()
    if config.ReadBool('ShowInspector'):
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
