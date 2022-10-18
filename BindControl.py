#!/usr/bin/env python3

import wx
import wx.lib.mixins.inspection
import wx.adv
import wx.html

from pathlib import Path
from Profile import Profile
from UI.PrefsDialog import PrefsDialog

###################
# Main Window Class
###################
class Main(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title = "BindControl")

        self.about_info = None

        self.LogWindow = wx.LogWindow(self, "Log Window", show = False, passToOld = False)

        # Start with a new profile
        self.Profile = Profile(self)

        config = wx.FileConfig('bindcontrol')
        wx.ConfigBase.Set(config)
        # Check each config bit for existence and set to default if no
        if not config.Exists('BindPath'):
            if wx.Platform == '__WXMSW__':
                bindpath = "C:\\cohbinds\\"
            else:
                bindpath = str(Path.home().joinpath('cohbinds'))
            config.Write('BindPath', bindpath)
        if not config.Exists('GameBindPath'):
            if wx.Platform != '__WXMSW__':
                config.Write('GameBindPath', "Z:\\cohbinds\\")
        if not config.Exists('ResetKey')        : config.Write('ResetKey', 'LCTRL+R')
        if not config.Exists('UseSplitModKeys') : config.WriteBool('UseSplitModKeys', False)
        if not config.Exists('FlushAllBinds')   : config.WriteBool('FlushAllBinds', True)
        if not config.Exists('StartWith')       : config.Write('StartWith', 'New Profile')
        config.Flush()

        self.PrefsDialog = PrefsDialog(self)

        # "Profile" Menu
        ProfMenu = wx.Menu()

        Profile_new   = ProfMenu.Append(-1, "New Profile...", "Create a new profile")
        Profile_load  = ProfMenu.Append(-1, "Load Profile...", "Load an existing profile")
        Profile_save  = ProfMenu.Append(-1, "Save Profile", "Save the current profile")
        ProfMenu.AppendSeparator()
        Profile_preferences = ProfMenu.Append(wx.ID_PREFERENCES, "&Preferences", "Configure BindControl")
        Profile_exit  = ProfMenu.Append(wx.ID_EXIT)

        Profile_new.Enable(False)

        # "Help" Menu
        HelpMenu = wx.Menu()

        Help_manual  = HelpMenu.Append(-1,"Manual","User's Manual")
        Help_faq     = HelpMenu.Append(-1,"FAQ","Frequently Asked Questions")
        Help_license = HelpMenu.Append(-1,"License Info","")
        Help_about   = HelpMenu.Append(wx.ID_ABOUT)

        Help_manual.Enable(False)
        Help_faq.Enable(False)
        Help_license.Enable(False)

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
        self.Bind(wx.EVT_MENU , None                       , Profile_new)
        self.Bind(wx.EVT_MENU , self.Profile.LoadFromFile  , Profile_load)
        self.Bind(wx.EVT_MENU , self.Profile.SaveToFile    , Profile_save)
        self.Bind(wx.EVT_MENU , self.OnMenuPrefsDialog     , Profile_preferences)
        self.Bind(wx.EVT_MENU , self.OnMenuExitApplication , Profile_exit)

        self.Bind(wx.EVT_MENU, None, Help_manual)
        self.Bind(wx.EVT_MENU, None, Help_faq)
        self.Bind(wx.EVT_MENU, None, Help_license)
        self.Bind(wx.EVT_MENU, self.OnMenuAboutBox,      Help_about)

        self.Bind(wx.EVT_MENU, self.OnMenuLogWindow, Log_window)

        self.AppIcon = wx.Icon()
        self.AppIcon.LoadFile('icons/BindControl.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.AppIcon)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)

        # TODO open with no profile, force "new" or "load"
        # Probably want Profile() to return something to fill the sizer
        self.Sizer.Add(self.Profile, 1, wx.EXPAND | wx.ALL, 3)

        # WRITE BUTTON
        WriteButton = wx.Button(self, -1, "Write Binds")
        self.Sizer.Add(WriteButton, 0, wx.EXPAND | wx.ALL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnWriteBindsButton, WriteButton)

        self.SetSizerAndFit(self.Sizer)

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
            info.SetIcon(self.AppIcon)
            info.SetName('BindControl')
            info.SetVersion('0.5')
            info.SetDescription("""
BindControl can help you set up custom keybinds in City of Heroes/Villains, including speed-on-demand binds.

Based on CityBinder 0.76, Copyright (C) 2005-2006 Jeff Sheets

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

class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        self.Init()
        main = Main(None)
        main.Show()

        return True

if __name__ == "__main__":
    app = MyApp(redirect=False)

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()

