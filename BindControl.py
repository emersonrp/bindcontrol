#!/usr/bin/env python3
import sys, os, platform, re

import wx
import wx.lib.mixins.inspection
import wx.adv
import wx.html
from bcVersion import current_version

from pathlib import Path
from Profile import Profile
from UI.PrefsDialog import PrefsDialog
from Help import ShowHelpWindow
from UI.ControlGroup import cgTextCtrl, cgButton

###################
# Main Window Class
###################
class Main(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title = "BindControl")

        self.about_info = None

        self.LogWindow = wx.LogWindow(self, "Log Window", show = False, passToOld = False)
        self.LogWindow.SetLogLevel(wx.LOG_Message)
        self.LogWindow.GetFrame().SetSize(1000,300)

        config = wx.FileConfig('bindcontrol')
        wx.ConfigBase.Set(config)
        # Check each config bit for existence and set to default if no
        if not config.Exists('BindPath'):
            if platform.system() == 'Windows':
                bindpath = "C:\\coh\\"
            else:
                bindpath = str(Path.home() / '.wine' / 'drive_c' / 'coh')
            config.Write('BindPath', bindpath)
        if not config.Exists('GameBindPath'):
            if platform.system() != 'Windows':
                config.Write('GameBindPath', "c:\\coh\\")
        if not config.Exists('ResetKey')            : config.Write('ResetKey', 'LCTRL+R')
        if not config.Exists('UseSplitModKeys')     : config.WriteBool('UseSplitModKeys', False)
        if not config.Exists('FlushAllBinds')       : config.WriteBool('FlushAllBinds', True)
        if not config.Exists('StartWith')           : config.Write('StartWith', 'Last Profile')
        if not config.Exists('ProfilePath')         : config.Write('ProfilePath', str(Path.home() / "Documents" / "bindcontrol"))
        if not config.Exists('SaveSizeAndPosition') : config.WriteBool('SaveSizeAndPosition', True)
        if not config.Exists('VerboseBLF')          : config.WriteBool('VerboseBLF', False)
        if not config.Exists('CrashOnBindError')    : config.WriteBool('CrashOnBindError', False)
        if not config.Exists('ShowInspector')       : config.WriteBool('ShowInspector', False)
        config.Flush()

        self.Sizer = wx.BoxSizer(wx.VERTICAL)

        # Start with a new profile

        self.Profile = Profile(self)

        self.Sizer.Add(self.Profile, 1, wx.EXPAND)

        # load up the last one if the pref says to and if it's there
        if config.Read('StartWith') == 'Last Profile':
            filename = config.Read('LastProfile')
            if filename:
                self.Profile.doLoadFromFile(filename)


        self.PrefsDialog = PrefsDialog(self)

        # "Profile" Menu
        ProfMenu = wx.Menu()

        Profile_new         = ProfMenu.Append(-1, "New Profile", "Create a new profile")
        Profile_load        = ProfMenu.Append(-1, "Load Profile...", "Load an existing profile")
        Profile_save        = ProfMenu.Append(-1, "&Save Profile\tCTRL-S", "Save the current profile")
        Profile_saveas      = ProfMenu.Append(-1, "Save Profile As...", "Save the current profile under a new filename")
        ProfMenu.AppendSeparator()
        Profile_savedefault = ProfMenu.Append(-1, "Save Profile As Default", "Save the current profile as the default for new profiles")
        ProfMenu.AppendSeparator()
        Profile_preferences = ProfMenu.Append(wx.ID_PREFERENCES, "&Preferences", "Configure BindControl")
        Profile_exit  = ProfMenu.Append(wx.ID_EXIT)

        # "Help" Menu
        HelpMenu = wx.Menu()

        Help_manual  = HelpMenu.Append(-1,"Manual","User's Manual")
        Help_faq     = HelpMenu.Append(-1,"FAQ","Frequently Asked Questions")
        Help_files   = HelpMenu.Append(-1,"Files","About BindControl's Output Files")
        Help_license = HelpMenu.Append(-1,"License Info","")
        Help_about   = HelpMenu.Append(wx.ID_ABOUT)

        Help_faq.Enable(False)

        LogMenu = wx.Menu()

        Log_window = LogMenu.Append(-1, "Log Window", "Show the log window")

        # cram the separate menus into a menubar
        MenuBar = wx.MenuBar()
        MenuBar.Append(ProfMenu, 'Profile')
        MenuBar.Append(HelpMenu, 'Help')
        MenuBar.Append(LogMenu, 'Log')

        # glue the menubar into the main window
        self.SetMenuBar(MenuBar)

        # MENUBAR EVENTS
        self.Bind(wx.EVT_MENU , self.OnNewProfile          , Profile_new)
        self.Bind(wx.EVT_MENU , self.OnProfileLoad         , Profile_load)
        self.Bind(wx.EVT_MENU , self.OnProfileSave         , Profile_save)
        self.Bind(wx.EVT_MENU , self.OnProfileSaveAs       , Profile_saveas)
        self.Bind(wx.EVT_MENU , self.OnProfileSaveDefault  , Profile_savedefault)
        self.Bind(wx.EVT_MENU , self.OnMenuPrefsDialog     , Profile_preferences)
        self.Bind(wx.EVT_MENU , self.OnMenuExitApplication , Profile_exit)

        self.Bind(wx.EVT_MENU, self.OnHelpManual, Help_manual)
        self.Bind(wx.EVT_MENU, None, Help_faq)
        self.Bind(wx.EVT_MENU, self.OnHelpFiles, Help_files)
        self.Bind(wx.EVT_MENU, self.OnHelpLicense, Help_license)
        self.Bind(wx.EVT_MENU, self.OnMenuAboutBox,      Help_about)

        self.Bind(wx.EVT_MENU, self.OnMenuLogWindow, Log_window)

        self.AppIcon = wx.IconBundle()
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        filename = f"{base_path}/icons/BindControl.ico"
        self.AppIcon.AddIcon(filename, wx.BITMAP_TYPE_ANY)
        self.SetIcons(self.AppIcon)

        # BUTTONS
        self.ProfDirButton = cgButton(self, -1, "Set Binds Location")
        self.ProfDirButton.SetToolTip("Configure the location where this Profile will write bindfiles")
        WriteButton = wx.Button(self, -1, "Write Binds")
        WriteButton.SetToolTip("Write out the bindfiles to the configured binds directory")
        DeleteButton = wx.Button(self, -1, "Delete All Binds")
        DeleteButton.SetToolTip("Delete all BindControl-managed files in the configured binds directory")
        writeSizer = wx.BoxSizer(wx.HORIZONTAL)
        writeSizer.Add(self.ProfDirButton, 0, wx.EXPAND)
        writeSizer.Add(WriteButton, 1, wx.EXPAND)
        writeSizer.Add(DeleteButton, 0, wx.EXPAND)
        self.Sizer.Add(writeSizer,  0, wx.EXPAND | wx.ALL, 10)
        self.ProfDirButton.Bind(wx.EVT_BUTTON, self.OnProfDirButton)
        WriteButton  .Bind(wx.EVT_BUTTON, self.OnWriteBindsButton)
        DeleteButton .Bind(wx.EVT_BUTTON, self.OnDeleteBindsButton)

        # Do not SetSizerAndFit() - Fit() is poison
        self.SetSizer(self.Sizer)

        if config.ReadBool('SaveSizeAndPosition') and config.HasEntry('WinH') and config.HasEntry('WinW'):
            height = config.ReadInt('WinH')
            width  = config.ReadInt('WinW')
        else:
            height = self.Profile.GetBestSize().height
            width  = self.Profile.GetBestSize().width + 24 # account for Profile's padding

        self.SetSize((width, height))

        if config.ReadBool('SaveSizeAndPosition') and config.HasEntry('WinX') and config.HasEntry('WinY'):
            self.SetPosition((config.ReadInt('WinX'), config.ReadInt('WinY')))

        self.Bind(wx.EVT_CLOSE, self.OnWindowClosing)
        self.CheckProfDirButtonErrors()

    def OnNewProfile(self, _):
        if self.Profile and self.Profile.Modified:
            result = wx.MessageBox("Profile not saved, save now?", "Profile modified", wx.YES_NO|wx.CANCEL)
            if result == wx.YES:
                self.Profile.doSaveToFile()
            elif result == wx.CANCEL:
                return

        dlg = wx.TextEntryDialog(self, 'Enter name for new profile:')
        if dlg.ShowModal() == wx.ID_OK:
            # check if we already have a bind named that.  Complex Binds use the name as
            # part of the bindfiles' filenames, so we can't have dupes
            newname = dlg.GetValue()
        else:
            return

        self.Freeze()
        try:
            self.Sizer.Remove(0)
            self.Profile.Destroy()

            self.Profile = Profile(self)
            self.Sizer.Insert(0, self.Profile, 1, wx.EXPAND)

            self.Profile.LoadFromDefault(newname)

        except Exception as e:
            wx.LogError(f"Something broke in new profile: {e}")
        finally:
            self.CheckProfDirButtonErrors()
            self.Layout()
            self.Thaw()

    def OnProfileLoad(self, evt):
        self.Profile.LoadFromFile(evt)
        self.CheckProfDirButtonErrors()
    def OnProfileSave(self, evt)      : self.Profile.doSaveToFile(evt)
    def OnProfileSaveAs(self, evt)    : self.Profile.SaveToFile(evt)
    def OnProfileSaveDefault(self, _) : self.Profile.SaveAsDefault()

    def OnProfDirButton(self, _ = None):
        ProfDirDialog = wx.Dialog(self, -1, "Set Binds Location")

        sizer = wx.BoxSizer(wx.VERTICAL)
        ProfDirDialog.SetSizer(sizer)

        sizer.Add(wx.StaticText(ProfDirDialog, -1, "Select the location where this profile will write its bindfiles:"), 1, wx.EXPAND|wx.ALL, 10)

        config = wx.ConfigBase.Get()
        bindpath = config.Read('BindPath')
        separator = "\\" if platform.system() == "Windows" else "/"

        dirSizer = wx.BoxSizer(wx.HORIZONTAL)
        dirSizer.Add(wx.StaticText(ProfDirDialog, -1,
                    f"{bindpath}{separator}"), 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
        PathText = cgTextCtrl(ProfDirDialog, -1, value = self.Profile.ProfileBindsDir)
        dirSizer.Add(PathText, 1, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        PathText.Bind(wx.EVT_TEXT, self.OnPathTextChanged)

        sizer.Add(dirSizer, 1, wx.EXPAND)

        sizer.Add(wx.StaticText(ProfDirDialog, -1, "Changing this value will automatically save the Profile,\nincluding any other changes you have made."), 1, wx.EXPAND|wx.ALL, 10)

        buttonsizer = ProfDirDialog.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL)

        sizer.Add(buttonsizer, 1, wx.EXPAND|wx.ALL, 10)

        ProfDirDialog.Layout()

        PathText.ClearErrors() # whyyyy?
        ### TODO - instead of re-calling OnProfDirButton() from scratch each time, break this dialog-show
        ### out into its own method and just re-show the dialog as needed.  Maybe this all wants its own class.
        with ProfDirDialog as dlg:
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                newvalue = PathText.GetValue()
                # call us again if we tried to OK an error state
                if PathText.HasErrors(): return self.OnProfDirButton()
                # if we changed the directory, offer to delete the old one.
                if self.Profile.ProfileBindsDir and (newvalue != self.Profile.ProfileBindsDir):
                    answer = wx.MessageBox(
                            f'Binds Location changed.  Delete old binds directory {self.Profile.BindsDir()}?',
                            'Binds Location Changed',wx.YES_NO, self
                    )
                    if answer == wx.YES:
                        self.Profile.doDeleteBindFiles(self.Profile.AllBindFiles())
                self.Profile.ProfileBindsDir = newvalue
                self.Profile.doSaveToFile()

        # need this out here in case we cancelled on a previously-blank one.
        # This is very very unlikely to happen and awful if it does.
        if PathText.HasErrors(): return self.OnProfDirButton()

        self.CheckProfDirButtonErrors()

    def CheckProfDirButtonErrors(self):
        if self.Profile.ProfileBindsDir:
            self.ProfDirButton.RemoveError('undef')
        else:
            self.ProfDirButton.AddError('undef', 'Your binds directory is unset.  Binds cannot be written.')

        if len(self.Profile.ProfileBindsDir) <= 8:
            self.ProfDirButton.RemoveWarning('toolong')
        else:
            self.ProfDirButton.AddWarning('toolong', 'Your binds directory name is rather long.  This is not an error but can lead to some binds being too long for the game to use.')


    def OnPathTextChanged(self, evt):
        textctrl = evt.EventObject
        value = textctrl.GetValue()

        if not value:
            textctrl.AddError('undef', 'You must specify a short, unique bindfile directory name.')
        else:
            textctrl.RemoveError('undef')

        if re.search(r'\s', value):
            textctrl.AddError('spaces', 'The binds directory cannot contain spaces.')
        else:
            textctrl.RemoveError('spaces')

        # TODO this is two places, make it a helper method somewhere
        if value.upper() in [
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM0',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9', 'LPT0',
        ]:
            textctrl.AddError('reserved', 'The name you have selected is a reserved filename in Windows.  Please select another.')
        else:
            textctrl.RemoveError('reserved')

    def OnWriteBindsButton(self, _):
        self.Profile.WriteBindFiles()

    def OnDeleteBindsButton(self, _):
        self.Profile.DeleteBindFiles()

    def OnMenuPrefsDialog(self, _):
        if self.PrefsDialog.ShowModal() == wx.ID_OK:
            config = wx.ConfigBase.Get()
            config.Write('BindPath', self.PrefsDialog.bindsDirPicker.GetPath())
            if self.PrefsDialog.gameBindsDirPicker:
                config.Write('GameBindPath', self.PrefsDialog.gameBindsDirPicker.GetValue())
            config.WriteBool('UseSplitModKeys', self.PrefsDialog.UseSplitModKeys.GetValue())
            config.WriteBool('FlushAllBinds', self.PrefsDialog.FlushAllBinds.GetValue())
            config.Write('ResetKey', self.PrefsDialog.ResetKey.GetLabel())

            startwith = "New Profile" if self.PrefsDialog.StartWithNewProfile.GetValue() else "Last Profile"
            config.Write('StartWith', startwith)
            config.Write('ProfilePath', self.PrefsDialog.ProfileDirPicker.GetPath())

            config.WriteBool('SaveSizeAndPosition', self.PrefsDialog.SaveSizeAndPosition.GetValue())

            config.Write('ControllerMod1', self.PrefsDialog.ControllerModPicker1.GetStringSelection())
            config.Write('ControllerMod2', self.PrefsDialog.ControllerModPicker2.GetStringSelection())
            config.Write('ExtraMod1', self.PrefsDialog.ExtraModPicker1.GetStringSelection())
            config.Write('ExtraMod2', self.PrefsDialog.ExtraModPicker2.GetStringSelection())
            config.Write('ExtraMod3', self.PrefsDialog.ExtraModPicker3.GetStringSelection())
            config.Write('ExtraMod4', self.PrefsDialog.ExtraModPicker4.GetStringSelection())

            config.WriteBool('VerboseBLF', self.PrefsDialog.VerboseBLF.GetValue())
            config.WriteBool('CrashOnBindError', self.PrefsDialog.CrashOnBindError.GetValue())
            config.WriteBool('ShowInspector', self.PrefsDialog.ShowInspector.GetValue())

            config.Flush()

    def OnMenuAboutBox(self, _):
        if self.about_info is None:
            info = wx.adv.AboutDialogInfo()
            info.AddDeveloper('R Pickett (emerson@hayseed.net)')
            info.SetName('BindControl')
            info.SetVersion(current_version())
            info.SetDescription((
                "BindControl can help you set up custom keybinds in City of Heroes/Villains, including speed-on-demand binds.\n\n"

                "Based on CityBinder 0.76, Copyright (c) 2005-2006 Jeff Sheets, and CityBinder for Homecoming 0.2, Copyright (c) 2021-2023 tailcoat\n\n"

                "Speed-On-Demand binds were originally created by Gnarley's Speed On Demand Binds Program.  Advanced Teleport Binds originally by DrLetharga, updated for Homecoming by emerson.\n\n"

                "Mastermind binds originally by Sandolphan in CoV beta, later updated by Konoko.\n\n"

                "Inspiration Popper design adapted from CityBinder for Homecoming by Tailcoat."
            ))
            info.SetCopyright('(c) 2010-2024 R Pickett <emerson@hayseed.net>')
            info.SetWebSite('https://github.com/emersonrp/bindcontrol')
            self.about_info = info

        wx.adv.AboutBox(self.about_info)

    def OnMenuLogWindow(self, _):
        self.LogWindow.Show()

    def OnMenuExitApplication(self, _):
        self.Close()

    def OnHelpManual(self, _):
        ShowHelpWindow(self, 'Manual.html')

    def OnHelpLicense(self, _):
        ShowHelpWindow(self, 'LICENSE.html')

    def OnHelpFiles(self, _):
        ShowHelpWindow(self, 'OutputFiles.html')

    def OnWindowClosing(self, evt):
        if self.Profile.Modified:
            result = wx.MessageBox("Profile not saved, save now?", "Profile modified",wx.YES_NO|wx.CANCEL)
            if result == wx.YES:
                self.Profile.doSaveToFile()
            elif result == wx.CANCEL:
                return

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

        self.Profile = None

        self.Init()
        self.Main = Main(None)
        self.Profile = self.Main.Profile

        # TODO bootstrapping problem, can't do this inside Profile's "__init__" because
        # it needs to be defined deep inside its innards.  This is amateur hour stuff sigh.
        self.Profile.CheckAllConflicts()

        self.Main.Show()

        return True

if __name__ == "__main__":
    app = MyApp(redirect=False)

    config = wx.ConfigBase.Get()
    if config.ReadBool('ShowInspector'):
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
