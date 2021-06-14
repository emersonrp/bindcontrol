#!/usr/bin/env python3

import wx
import wx.lib.mixins.inspection
import wx.adv

from Profile import Profile
import StdDefault

#import Powerbinder
#import PowerBindCmds

###################
# Main Window Class
###################
class Main(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title = "BindControl")

        self.about_info = None

        # Start with a new profile
        self.Profile = Profile(self)

        ProfMenu = wx.Menu()

        Profile_new   = ProfMenu.Append(-1, "New Profile...", "Create a new profile")
        Profile_load  = ProfMenu.Append(-1, "Load Profile...", "Load an existing profile")
        Profile_save  = ProfMenu.Append(-1, "Save Profile", "Save the current profile")
        ProfMenu.AppendSeparator()
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

        # cram the separate menus into a menubar
        MenuBar = wx.MenuBar()
        MenuBar.Append(ProfMenu, 'Profile')
        MenuBar.Append(HelpMenu, 'Help')

        # glue the menubar into the main window
        self.SetMenuBar(MenuBar)

        # MENUBAR EVENTS
        self.Bind(wx.EVT_MENU, None, Profile_new)
        self.Bind(wx.EVT_MENU, self.Profile.LoadFromFile, Profile_load)
        self.Bind(wx.EVT_MENU, self.Profile.SaveToFile  , Profile_save)
        self.Bind(wx.EVT_MENU, self.OnMenuExitApplication, Profile_exit)

        self.Bind(wx.EVT_MENU, None, Help_manual)
        self.Bind(wx.EVT_MENU, None, Help_faq)
        self.Bind(wx.EVT_MENU, None, Help_license)
        self.Bind(wx.EVT_MENU, self.OnMenuAboutBox,      Help_about)

        AppIcon = wx.Icon()
        AppIcon.LoadFile('BindControl.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(AppIcon)

        # TODO - read in the config for the window (size, location, etc)
        # and apply it before ->Show()

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.Profile, 1, wx.EXPAND |  wx.ALL, 3)

        WriteButton = wx.Button(self, -1, "Write Binds")
        sizer.Add(WriteButton, 0, wx.EXPAND | wx.ALL, 10)

        # WRITE BUTTON EVENT
        self.Bind(wx.EVT_BUTTON, self.OnWriteBindsButton, WriteButton)

        self.SetSizerAndFit(sizer)

    def OnWriteBindsButton(self, evt):
        self.Profile.WriteBindFiles()

    def OnMenuAboutBox(self, event):
        if self.about_info is None:
            info = wx.adv.AboutDialogInfo()
            info.AddDeveloper('R Pickett (emerson@hayseed.net)')
            info.SetName('BindControl')
            info.SetVersion('0.1')
            info.SetDescription("BindControl can help you set up custom keybinds in City of Heroes/Villains, including speed-on-demand binds.\n\nBased on CityBinder 0.76, Copyright (C) 2005-2006 Jeff Sheets\n\nSpeed-On-Demand binds were originally created by Gnarley\'s Speed On Demand Binds Program.  Advanced Teleport Binds by DrLetharga.")
            info.SetCopyright('(c) 2010-2021 R Pickett <emerson@hayseed.net>')
            info.SetWebSite('https://github.com/emersonrp/bindcontrol')
            self.about_info = info

        wx.adv.AboutBox(self.about_info)

    def OnMenuExitApplication(self, event):
        self.Close(1)

class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        self.Init()
        main = Main(None)
        main.Show()

        return True

if __name__ == "__main__":
    app = MyApp(redirect=False)
    app.MainLoop()

