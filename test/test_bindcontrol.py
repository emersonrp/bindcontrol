import BindControl
import pytest
import threading
import wx

from pathlib import Path
from Util.DefaultProfile import DefaultProfile

def test_create_main_no_config(config):
    stdpaths = wx.StandardPaths.Get()

    assert config.Read('GameLang') == 'English'
    assert config.Read('ResetKey') == 'CTRL+R'
    assert config.ReadBool('UseSplitModKeys') is False
    assert config.ReadBool('FlushAllBinds')
    assert config.Read('ProfilePath') == str(Path(stdpaths.GetDocumentsDir()) / "bindcontrol")
    assert config.ReadBool('StartWithLastProfile')
    assert config.ReadBool('SaveSizeAndPosition')
    assert not config.ReadBool('VerboseBLF')
    assert not config.ReadBool('CrashOnBindError')
    assert not config.ReadBool('ShowInspector')
    assert not config.ReadBool('ShowDebugMessages')
    assert config.ReadInt('WinH') == 1000
    assert config.ReadInt('WinW') == 1000
    assert config.Read('DefaultProfile') == DefaultProfile

def test_main_menubar(app):
    main = app.Main
    menubar = main.GetMenuBar()
    assert isinstance(menubar, wx.MenuBar)
    assert menubar.GetMenuCount() == 3
    profmenu = menubar.GetMenu(0)
    assert isinstance(profmenu, wx.Menu)
    assert profmenu.GetTitle() == 'Profile'
    assert profmenu.GetMenuItemCount() == 11
    assert profmenu.FindItemByPosition(0).GetItemLabel() == "&New Profile\tCTRL-N"
    assert profmenu.FindItemByPosition(1).GetItemLabel() == "&Load Profile...\tCTRL-L"
    assert profmenu.FindItemByPosition(2).GetItemLabel() == "&Import Saved Build...\tCTRL-I"
    assert profmenu.FindItemByPosition(3).GetItemLabel() == "&Save Profile\tCTRL-S"
    assert profmenu.FindItemByPosition(4).GetItemLabel() == "Save Profile As..."
    assert profmenu.FindItemByPosition(5).GetItemLabel() == "Close Profile"
    assert profmenu.FindItemByPosition(6).GetKind() == wx.ITEM_SEPARATOR
    assert profmenu.FindItemByPosition(7).GetItemLabel() == "Save Profile As Default"
    assert profmenu.FindItemByPosition(8).GetKind() == wx.ITEM_SEPARATOR
    assert profmenu.FindItemByPosition(9).GetItemLabel() == "&Preferences"
    assert profmenu.FindItemByPosition(10).GetItemLabel() == "&Quit"

    helpmenu = menubar.GetMenu(1)
    assert isinstance(helpmenu, wx.Menu)
    assert helpmenu.GetTitle() == 'Help'
    assert helpmenu.GetMenuItemCount() == 7
    assert helpmenu.FindItemByPosition(0).GetItemLabel() == "Manual"
    assert helpmenu.FindItemByPosition(1).GetItemLabel() == "Getting Started"
    assert helpmenu.FindItemByPosition(2).GetItemLabel() == "Output Files"
    assert helpmenu.FindItemByPosition(3).GetItemLabel() == "Bind Directories"
    assert helpmenu.FindItemByPosition(4).GetItemLabel() == "License Info"
    assert helpmenu.FindItemByPosition(5).GetItemLabel() == "Reporting Bugs"
    assert helpmenu.FindItemByPosition(6).GetItemLabel() == "&About"

    logmenu = menubar.GetMenu(2)
    assert isinstance(logmenu, wx.Menu)
    assert logmenu.GetTitle() == 'Log'
    assert logmenu.GetMenuItemCount() == 1
    assert logmenu.FindItemByPosition(0).GetItemLabel() == "Log Window"

def test_main_icons(app):
    main = app.Main
    iconbundle = main.GetIcons()
    assert isinstance(iconbundle, wx.IconBundle)
    assert iconbundle.GetIconCount() == 5
    for i in range(5):
        assert isinstance(iconbundle.GetIconByIndex(i), wx.Icon)

def test_main_bottombuttonpanel(app):
    main = app.Main
    assert isinstance(main.BottomButtonPanel, wx.Panel)
    buttons = main.BottomButtonPanel.GetChildren()
    assert main.ProfDirButton in buttons
    assert main.ProfDirButton.GetToolTipText() != ''
    assert main.WriteButton in buttons
    assert main.WriteButton.GetToolTipText() != ''
    assert main.DeleteButton in buttons
    assert main.DeleteButton.GetToolTipText() != ''

# This is not working yet -- I believe the mock is grabbing OnProfileImport
# after the Bind() in there already has a pointer to it.  This involves examining
# how Bind() works and seeing if this is at all even possible
@pytest.mark.skip
def test_main_menuevents(app, mocker):
    main = app.Main
    mocked_import = mocker.patch('BindControl.Main.OnProfileImport')
    menuevt = wx.CommandEvent(wx.wxEVT_MENU, main.Profile_import.GetId())
    wx.PostEvent(main, menuevt)
    mocked_import.assert_called()

#####
@pytest.fixture(autouse = True)
def config(app):
    config = wx.ConfigBase.Get()
    yield config

@pytest.fixture(autouse = True)
def app():
    app = MyApp()
    thread = threading.Thread(target = app.MainLoop)
    thread.start()
    return app

class MyApp(wx.App):
    def OnInit(self):
        wx.ConfigBase.Set(wx.FileConfig())
        self.Main = BindControl.Main(guiLogging = False)
        self.SetTopWindow(self.Main)
        return True
