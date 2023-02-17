#!/usr/bin/env python3
import sys, os
import wx
import wx.lib.mixins.inspection
import wx.adv
import wx.html

from pathlib import Path
from Profile import Profile
from UI.PrefsDialog import PrefsDialog
from Help import ShowHelpWindow

###################
# Main Window Class
###################
class Main(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title = "BindControl")

        self.about_info = None

        self.SetStatusBar(wx.StatusBar(self, style = 0))

        self.LogWindow = wx.LogWindow(self, "Log Window", show = False, passToOld = False)

        config = wx.FileConfig('bindcontrol')
        wx.ConfigBase.Set(config)
        # Check each config bit for existence and set to default if no
        if not config.Exists('BindPath'):
            if wx.Platform == '__WXMSW__':
                bindpath = "C:\\coh\\"
            else:
                bindpath = str(Path.home() / '.wine' / 'drive_c' / 'coh')
            config.Write('BindPath', bindpath)
        if not config.Exists('GameBindPath'):
            if wx.Platform != '__WXMSW__':
                config.Write('GameBindPath', "c:\\coh\\")
        if not config.Exists('ResetKey')        : config.Write('ResetKey', 'LCTRL+R')
        if not config.Exists('UseSplitModKeys') : config.WriteBool('UseSplitModKeys', False)
        if not config.Exists('FlushAllBinds')   : config.WriteBool('FlushAllBinds', True)
        if not config.Exists('StartWith')       : config.Write('StartWith', 'New Profile')
        config.Flush()

        # Start with a new profile
        self.Profile = Profile(self)
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
        self.Bind(wx.EVT_MENU, self.OnHelpLicense, Help_license)
        self.Bind(wx.EVT_MENU, self.OnMenuAboutBox,      Help_about)

        self.Bind(wx.EVT_MENU, self.OnMenuLogWindow, Log_window)

        self.AppIcon = wx.IconBundle()
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        filename = f"{base_path}/icons/BindControl.ico"
        self.AppIcon.AddIcon(filename, wx.BITMAP_TYPE_ANY)
        self.SetIcons(self.AppIcon)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)

        self.Sizer.Add(self.Profile, 1, wx.EXPAND | wx.ALL, 3)

        # WRITE BUTTON
        WriteButton = wx.Button(self, -1, "Write Binds")
        self.Sizer.Add(WriteButton, 0, wx.EXPAND | wx.ALL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnWriteBindsButton, WriteButton)

        self.SetSizerAndFit(self.Sizer)

        self.Bind(wx.EVT_CLOSE, self.OnWindowClosing)

    def OnNewProfile(self, _):
        if self.Profile.Modified:
            result = wx.MessageBox("Profile not saved, save now?", "Profile modified", wx.YES_NO|wx.CANCEL)
            if result == wx.YES:
                self.Profile.doSaveToFile()
            elif result == wx.CANCEL:
                return
        self.Freeze()
        try:
            self.Sizer.Remove(0)
            self.Profile.Destroy()
            self.Profile = Profile(self)
            self.Sizer.Insert(0, self.Profile, 1, wx.EXPAND|wx.ALL, 3)
            defaultProfile = Path(self.Profile.ProfilePath() / 'Default.bcp')
            self.Profile.doLoadFromFile(defaultProfile)
        except Exception as e:
            wx.LogError(f"Something broke in new profile: {e}")
        finally:
            self.Layout()
            self.Thaw()

    def OnProfileLoad(self, evt)        :
        self.OnNewProfile(evt)
        self.Profile.LoadFromFile(evt)
    def OnProfileSave(self, evt)        : self.Profile.doSaveToFile(evt)
    def OnProfileSaveAs(self, evt)      : self.Profile.SaveToFile(evt)
    def OnProfileSaveDefault(self, evt) : self.Profile.SaveAsDefault(evt)

    def OnWriteBindsButton(self, _):
        self.Profile.WriteBindFiles()

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

            config.Flush()

    def OnMenuAboutBox(self, _):
        if self.about_info is None:
            info = wx.adv.AboutDialogInfo()
            info.AddDeveloper('R Pickett (emerson@hayseed.net)')
            info.SetName('BindControl')
            info.SetVersion('0.9')
            info.SetDescription("""
BindControl can help you set up custom keybinds in City of Heroes/Villains, including speed-on-demand binds.

Based on CityBinder 0.76, Copyright (c) 2005-2006 Jeff Sheets

Speed-On-Demand binds were originally created by Gnarley's Speed On Demand Binds Program.  Advanced Teleport Binds by DrLetharga.

Mastermind binds originally by Sandolphan in CoV beta, later updated by Konoko.
""")
            info.SetCopyright('(c) 2010-2022 R Pickett <emerson@hayseed.net>')
            info.SetWebSite('https://github.com/emersonrp/bindcontrol')
            self.about_info = info

        wx.adv.AboutBox(self.about_info)

    def OnMenuLogWindow(self, _):
        self.LogWindow.Show()

    def OnMenuExitApplication(self, _):
        self.Close(True)

    def OnHelpManual(self, _):
        ShowHelpWindow(self, 'Manual.html')

    def OnHelpLicense(self, _):
        ShowHelpWindow(self, 'LICENSE.html')

    def OnWindowClosing(self, evt):
        if self.Profile.Modified:
            result = wx.MessageBox("Profile not saved, save now?", "Profile modified",wx.YES_NO|wx.CANCEL)
            if result == wx.YES:
                self.Profile.doSaveToFile()
            elif result == wx.CANCEL:
                return
        evt.Skip()

class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        self.Init()
        self.Main = Main(None)
        self.Profile = self.Main.Profile

        self.Main.Show()

        return True

if __name__ == "__main__":
    app = MyApp(redirect=False)

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()

