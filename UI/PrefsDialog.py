import platform
import re
from typing import Any, TYPE_CHECKING

import wx
import wx.lib.stattext as ST
from pathlib import Path, PureWindowsPath
from pubsub import pub

from Help import HelpButton
from UI.KeySelectDialog import bcKeyButton
from UI.ControlGroup import cgDirPickerCtrl, cgTextCtrl
from bcController import bcController

# This ST.GenStaticText is so we can intercept clicks on it, but
# the background color is wrong on Windows in a way I can't work out,
# and clicks work with wx.StaticText on Windows anyway, so...
if TYPE_CHECKING or platform.system() != 'Windows':
    class CBLabel(ST.GenStaticText):
        CB : Any = None
else:
    class CBLabel(wx.StaticText):
        CB : Any = None

class PrefsDialog(wx.Dialog):
    def __init__(self, parent) -> None:
        super().__init__(parent, title = "Preferences")

        config = wx.ConfigBase.Get()

        overallSizer = wx.BoxSizer(wx.VERTICAL)

        controller = bcController()

        notebook = wx.Notebook(self)

        ###
        # GENERAL PANEL
        ###
        self.generalPanel = wx.Panel(notebook)
        generalSizer = wx.BoxSizer(wx.VERTICAL)

        gameDirSizer = wx.StaticBoxSizer(wx.VERTICAL, self.generalPanel, 'Paths and Directories')
        gameDirBox = gameDirSizer.GetStaticBox()

        gameDirGrid = wx.FlexGridSizer(2, 0, 0)

        gameDirGrid.Add(wx.StaticText(gameDirBox, label = 'Binds Directory Location:'), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)

        gameDirRBSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.gameDirInsideRB = wx.RadioButton(gameDirBox, label = 'Inside Game Directory')
        self.gameDirInsideRB.Bind(wx.EVT_RADIOBUTTON, self.OnDirPickerChange)
        self.gameDirInsideRB.SetValue(config.ReadBool('RelativeBindsDir'))
        gameDirRBSizer.Add(self.gameDirInsideRB, 0, wx.ALL|wx.ALIGN_CENTER, 6)
        self.gameDirAbsoluteRB = wx.RadioButton(gameDirBox, label = 'Absolute Path')
        self.gameDirAbsoluteRB.Bind(wx.EVT_RADIOBUTTON, self.OnDirPickerChange)
        self.gameDirAbsoluteRB.SetValue(not config.ReadBool('RelativeBindsDir'))
        gameDirRBSizer.Add(self.gameDirAbsoluteRB, 0, wx.ALL|wx.ALIGN_CENTER, 6)
        gameDirRBSizer.Add(HelpButton(gameDirBox, 'BindsDirLocation.html'))

        gameDirGrid.Add(gameDirRBSizer, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        self.bindsDirTextLabel = wx.StaticText(gameDirBox, label = 'Binds Directory:')
        gameDirGrid.Add(self.bindsDirTextLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.bindsDirText = cgTextCtrl(gameDirBox, value = config.Read('BindTextPath'), size = (300, -1))
        self.bindsDirText.DefaultToolTip = 'Bind files will be written to this subdirectory, inside your game directory.'
        self.bindsDirText.Bind(wx.EVT_TEXT, self.OnDirPickerChange)
        gameDirGrid.Add(self.bindsDirText, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        self.bindsDirPickerLabel = wx.StaticText(gameDirBox, label = 'Binds Directory:')
        gameDirGrid.Add(self.bindsDirPickerLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.bindsDirPicker = cgDirPickerCtrl(gameDirBox, path = config.Read('BindPath'), size = (300, -1))
        deftt = 'Bind files will be written to this subdirectory.'
        if platform.system() == 'Windows':
            deftt = deftt + '  Keeping this path as short as possible is strongly recommended.'
        self.bindsDirPicker.DefaultToolTip = deftt
        self.bindsDirPicker.UpdateTextCtrlFromPicker()
        self.bindsDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPickerChange)
        gameDirGrid.Add(self.bindsDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        self.gameBindsDirPicker = None
        self.gameBindsDirPickerLabel = None
        if (platform.system() != 'Windows'):
            self.gameBindsDirPickerLabel = wx.StaticText(gameDirBox, label = "In-Game Binds Directory:")
            gameDirGrid.Add(self.gameBindsDirPickerLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
            self.gameBindsDirPicker = cgTextCtrl(gameDirBox, value = config.Read('GameBindPath'))
            self.gameBindsDirPicker.DefaultToolTip = 'When playing via Wine, the in-game file paths will be different than the native ones.  Put a Windows path into this box that describes where Wine will find the above directory.  Keeping this path as short as possible is strongly recommended.  Check "Help > Getting Started with BindControl" for more information.'
            self.gameBindsDirPicker.Bind(wx.EVT_TEXT, self.OnGameBindsDirPickerChanged)
            gameDirGrid.Add(self.gameBindsDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        gameDirGrid.Add(wx.StaticText(gameDirBox, label = 'Homecoming Game Directory:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        gameDirPickerBox = wx.BoxSizer(wx.HORIZONTAL)
        self.gameDirPicker = cgDirPickerCtrl(gameDirBox, path = config.Read('GamePath'), size = (300, -1))
        self.gameDirPicker.DefaultToolTip = 'This is where Homecoming is located.  Leave blank if you don\'t have Homecoming installed.'
        self.gameDirPicker.UpdateTextCtrlFromPicker()
        self.gameDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPickerChange)
        gameDirPickerBox.Add(self.gameDirPicker, 0, wx.RIGHT, 6)
        gameDirPickerBox.Add(HelpButton(gameDirBox, 'HomecomingPath.html'))
        gameDirGrid.Add(gameDirPickerBox, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        gameDirGrid.Add(wx.StaticText(gameDirBox, label = 'Rebirth Game Directory:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        gameDirRebirthPickerBox = wx.BoxSizer(wx.HORIZONTAL)
        self.gameDirRebirthPicker = cgDirPickerCtrl(gameDirBox, path = config.Read('GameRebirthPath'), size = (300, -1))
        self.gameDirRebirthPicker.DefaultToolTip = 'This is where Rebirth is located.  Leave blank if you don\'t have Rebirth installed.'
        self.gameDirRebirthPicker.UpdateTextCtrlFromPicker()
        self.gameDirRebirthPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPickerChange)
        gameDirRebirthPickerBox.Add(self.gameDirRebirthPicker, 0, wx.RIGHT, 6)
        gameDirRebirthPickerBox.Add(HelpButton(gameDirBox, 'RebirthPath.html'))
        gameDirGrid.Add(gameDirRebirthPickerBox, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        gameDirGrid.Add(wx.StaticText(gameDirBox, label = 'Game Language:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.gameLangPicker = wx.Choice(gameDirBox, choices = ['ChineseTraditional','English','French','German','Japanese','Korean','uk'])
        self.gameLangPicker.SetStringSelection(config.Read('GameLang'))
        self.gameLangPicker.SetToolTip('The language of your installed game.  This is necessary to manage popmenus correctly.')
        gameDirGrid.Add(self.gameLangPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        ProfilePathLabel = wx.StaticText(gameDirBox, label = "Path for saved profiles:")
        gameDirGrid.Add(ProfilePathLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ProfileDirPicker = cgDirPickerCtrl(gameDirBox, path = config.Read('ProfilePath'), size = (300, -1))
        self.ProfileDirPicker.SetToolTip('Profiles will be saved to this location.')
        self.ProfileDirPicker.UpdateTextCtrlFromPicker()
        self.ProfileDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPickerChange)
        gameDirGrid.Add(self.ProfileDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        gameDirSizer.Add(gameDirGrid, 0, wx.EXPAND|wx.ALL, 10)

        generalSizer.Add(gameDirSizer, 0, wx.EXPAND|wx.ALL, 10)

        optsSizer = wx.FlexGridSizer(2, 0, 0)

        optsSizer.Add(wx.StaticText(self.generalPanel, label = "Binds Reset Key:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        resetKey = config.Read('ResetKey')
        self.ResetKey = bcKeyButton(self.generalPanel, init ={ 'CtlName': 'ResetKey', 'Key' : resetKey })
        self.ResetKey.SetLabel(resetKey)
        self.ResetKey.DefaultToolTip = 'This is the key that will reset your binds to their default state, and stop all movement, if movement binds are installed.'
        optsSizer.Add(self.ResetKey, 1, wx.ALL|wx.ALIGN_CENTRE_VERTICAL, 6)

        splitKeyLabel = CBLabel(self.generalPanel, label = "Bind L/R mod keys separately:")
        optsSizer.Add(splitKeyLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.UseSplitModKeys = wx.CheckBox(self.generalPanel)
        self.UseSplitModKeys.SetValue(config.ReadBool('UseSplitModKeys'))
        self.UseSplitModKeys.SetToolTip("This allows the left and right modifier keys to be bound separately on the \"right-hand\" side of a bind.  Check \"Help > Getting Started with BindControl\" for more information.")
        optsSizer.Add(self.UseSplitModKeys, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        splitKeyLabel.CB = self.UseSplitModKeys
        splitKeyLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        flushBindsLabel = CBLabel(self.generalPanel, label = "Set binds to default on reset:")
        optsSizer.Add(flushBindsLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.FlushAllBinds = wx.CheckBox(self.generalPanel)
        self.FlushAllBinds.SetValue(config.ReadBool('FlushAllBinds'))
        self.FlushAllBinds.SetToolTip("Set all binds to City of Heroes' default before applying / resetting BindControl's binds.  Uncheck this if you have added any binds into the game that are not managed by BindControl.")
        optsSizer.Add(self.FlushAllBinds, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        flushBindsLabel.CB = self.FlushAllBinds
        flushBindsLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        StartWithLastProfileLabel = CBLabel(self.generalPanel, label = "On startup, load last used profile:")
        optsSizer.Add(StartWithLastProfileLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.StartWithLastProfile = wx.CheckBox(self.generalPanel)
        self.StartWithLastProfile.SetValue(config.ReadBool('StartWithLastProfile'))
        self.StartWithLastProfile.SetToolTip("Load the last profile you were working with when you start the program.")
        optsSizer.Add (self.StartWithLastProfile, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        StartWithLastProfileLabel.CB = self.StartWithLastProfile
        StartWithLastProfileLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        SaveSizeLabel = CBLabel(self.generalPanel, label = "Save size / position of window:")
        optsSizer.Add(SaveSizeLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.SaveSizeAndPosition = wx.CheckBox(self.generalPanel)
        self.SaveSizeAndPosition.SetValue(config.ReadBool('SaveSizeAndPosition'))
        self.SaveSizeAndPosition.SetToolTip("Save the size and position of the BindControl window between sessions.")
        optsSizer.Add(self.SaveSizeAndPosition, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        generalSizer.Add(optsSizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        SaveSizeLabel.CB = self.SaveSizeAndPosition
        SaveSizeLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        self.generalPanel.SetSizerAndFit(generalSizer)

        ###
        # CONTROLLER PANEL
        ###
        controllerPanel = wx.Panel(notebook)
        controllerSizer = wx.FlexGridSizer(3,0,0)

        # Controller name display
        controllerNameLabel = CBLabel(controllerPanel, label = 'Controller:')
        controllerSizer.Add(controllerNameLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        controllerName = CBLabel(controllerPanel, label = 'No controller detected!')
        if controller.GetNumberJoysticks() > 0:
            controllerName.SetLabel(controller.GetProductName())
        controllerSizer.Add(controllerName, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        controllerhelpbutton = HelpButton(controllerPanel, 'ControllerModifiers.html')
        controllerSizer.Add(controllerhelpbutton)

        # Pickers for controller_modifiers
        possible_mods = controller.ListOfPossibleMods()
        controllerModsLabel = CBLabel(controllerPanel, label = 'Controller Modifiers:')
        controllerSizer.Add(controllerModsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ControllerModPicker1 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ControllerModPicker1.SetStringSelection(config.Read('ControllerMod1'))
        controllerSizer.Add(self.ControllerModPicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ControllerModPicker2 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ControllerModPicker2.SetStringSelection(config.Read('ControllerMod2'))
        controllerSizer.Add(self.ControllerModPicker2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        # Pickers for extra_modifiers
        extraModsLabel = CBLabel(controllerPanel, label = 'Extra Modifiers:')
        controllerSizer.Add(extraModsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ExtraModPicker1 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ExtraModPicker1.SetStringSelection(config.Read('ExtraMod1'))
        controllerSizer.Add(self.ExtraModPicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ExtraModPicker2 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ExtraModPicker2.SetStringSelection(config.Read('ExtraMod2'))
        controllerSizer.Add(self.ExtraModPicker2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        controllerSizer.Add(wx.StaticText(controllerPanel, label = ''))
        self.ExtraModPicker3 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ExtraModPicker3.SetStringSelection(config.Read('ExtraMod3'))
        controllerSizer.Add(self.ExtraModPicker3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ExtraModPicker4 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ExtraModPicker4.SetStringSelection(config.Read('ExtraMod4'))
        controllerSizer.Add(self.ExtraModPicker4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        controllerPanel.SetSizerAndFit(controllerSizer)

        ###
        # DEBUG PANEL
        ###
        debugPanel = wx.Panel(notebook)
        debugSizer = wx.FlexGridSizer(2,0,0)

        verboseBLFLabel = CBLabel(debugPanel, label = "Verbose in-game feedback when loading bind file:")
        debugSizer.Add(verboseBLFLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.VerboseBLF = wx.CheckBox(debugPanel)
        self.VerboseBLF.SetValue(config.ReadBool('VerboseBLF'))
        tooltip = "Enable output to the chat box whenever a bind file is loaded.  This could be rather spammy, most especially with Speed on Demand binds."
        verboseBLFLabel.SetToolTip(tooltip)
        self.VerboseBLF.SetToolTip(tooltip)
        debugSizer.Add(self.VerboseBLF, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        verboseBLFLabel.CB = self.VerboseBLF
        verboseBLFLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        crashOnProfileErrorLabel = CBLabel(debugPanel, label = "Crash on loading profile error:")
        debugSizer.Add(crashOnProfileErrorLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.CrashOnProfileError = wx.CheckBox(debugPanel)
        self.CrashOnProfileError.SetValue(config.ReadBool('CrashOnProfileError'))
        tooltip = "Crash and raise a stack trace if there is an error loading a Profile.  You want this turned off unless you are doing deep debugging."
        crashOnProfileErrorLabel.SetToolTip(tooltip)
        self.CrashOnProfileError.SetToolTip(tooltip)
        debugSizer.Add(self.CrashOnProfileError, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        crashOnProfileErrorLabel.CB = self.CrashOnProfileError
        crashOnProfileErrorLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        crashOnBindErrorLabel = CBLabel(debugPanel, label = "Crash on write-binds error:")
        debugSizer.Add(crashOnBindErrorLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.CrashOnBindError = wx.CheckBox(debugPanel)
        self.CrashOnBindError.SetValue(config.ReadBool('CrashOnBindError'))
        tooltip = "Crash and raise a stack trace if there is an error writing the bind files.  You want this turned off unless you are doing deep debugging."
        crashOnBindErrorLabel.SetToolTip(tooltip)
        self.CrashOnBindError.SetToolTip(tooltip)
        debugSizer.Add(self.CrashOnBindError, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        crashOnBindErrorLabel.CB = self.CrashOnBindError
        crashOnBindErrorLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        VerboseCustomBindTitlesLabel = CBLabel(debugPanel, label = "Verbose Titles for Custom Binds:")
        debugSizer.Add(VerboseCustomBindTitlesLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.VerboseCustomBinds = wx.CheckBox(debugPanel)
        self.VerboseCustomBinds.SetValue(config.ReadBool('VerboseCustomBinds'))
        tooltip = "Show more information in the title of custom binds, including the bind type and bind ID."
        VerboseCustomBindTitlesLabel.SetToolTip(tooltip)
        self.VerboseCustomBinds.SetToolTip(tooltip)
        debugSizer.Add(self.VerboseCustomBinds, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        VerboseCustomBindTitlesLabel.CB = self.VerboseCustomBinds
        VerboseCustomBindTitlesLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        showInspectorLabel = CBLabel(debugPanel, label = "Show Widget Inspector (requires restart):")
        debugSizer.Add(showInspectorLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ShowInspector = wx.CheckBox(debugPanel)
        self.ShowInspector.SetValue(config.ReadBool('ShowInspector'))
        tooltip = "Show the wxPython widget inspector while running.  While harmless, this will open an extra, cryptic window that you're probably not interested in unless debugging."
        showInspectorLabel.SetToolTip(tooltip)
        self.ShowInspector.SetToolTip(tooltip)
        debugSizer.Add(self.ShowInspector, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        showInspectorLabel.CB = self.ShowInspector
        showInspectorLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        showDebugMessagesLabel = CBLabel(debugPanel, label = "Show debug messages in log window.")
        debugSizer.Add(showDebugMessagesLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ShowDebugMessages = wx.CheckBox(debugPanel)
        self.ShowDebugMessages.SetValue(config.ReadBool('ShowDebugMessages'))
        tooltip = "Show all debug messages in the Log Window.  This is harmless but might be spammy in some circumstances.  If you never look at the log window, you don't need to worry about this."
        showDebugMessagesLabel.SetToolTip(tooltip)
        self.ShowDebugMessages.SetToolTip(tooltip)
        debugSizer.Add(self.ShowDebugMessages, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        showDebugMessagesLabel.CB = self.ShowDebugMessages
        showDebugMessagesLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        debugPanel.SetSizerAndFit(debugSizer)

        notebook.AddPage(self.generalPanel, "General", select = True)
        notebook.AddPage(controllerPanel, "Controller")
        notebook.AddPage(debugPanel, "Debug")

        buttonSizer = wx.StdDialogButtonSizer()
        okbutton = wx.Button(self, wx.ID_OK)
        buttonSizer.AddButton(okbutton)
        buttonSizer.AddButton(wx.Button(self, wx.ID_CANCEL))
        okbutton.SetFocus()
        buttonSizer.Realize()

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(buttonSizer, 0, wx.ALL|wx.EXPAND, 10)

        overallSizer.Add(notebook, 0, wx.ALL|wx.EXPAND)
        overallSizer.Add(paddingSizer, 0, wx.ALL|wx.EXPAND)

        self.SetSizerAndFit(overallSizer)

        self.OnDirPickerChange()
        self.OnGameBindsDirPickerChanged()

    def OnDirPickerChange(self, evt = None) -> None:
        isRelativeDir = self.gameDirInsideRB.GetValue()

        self.bindsDirTextLabel.Show(isRelativeDir)
        self.bindsDirText.Show(isRelativeDir)
        self.bindsDirPickerLabel.Show(not isRelativeDir)
        self.bindsDirPicker.Show(not isRelativeDir)
        if self.gameBindsDirPicker and self.gameBindsDirPickerLabel:
            self.gameBindsDirPickerLabel.Show(not isRelativeDir)
            self.gameBindsDirPicker.Show(not isRelativeDir)
        self.generalPanel.Layout()

        # Check the gamedir picker
        gamedir = Path(self.gameDirPicker.GetPath())
        if gamedir.is_absolute():
            if gamedir.is_dir():
                self.gameDirPicker.RemoveError('exists')

                if ( Path(gamedir / 'bin').is_dir() and Path(gamedir / 'assets').is_dir()):
                    self.gameDirPicker.RemoveWarning('wrongdir')
                else:
                    self.gameDirPicker.AddWarning('wrongdir', f'The directory "{gamedir}" doesn\'t seem to have a Homecoming installation.')

            else:
                self.gameDirPicker.AddError('exists', f'The directory "{gamedir}" does not exist.')
        else:
            self.gameDirPicker.ClearErrors()

        # Check the rebirthdir picker
        rebirthdir = Path(self.gameDirRebirthPicker.GetPath())
        if rebirthdir.is_absolute():
            if rebirthdir.is_dir():
                self.gameDirRebirthPicker.RemoveError('exists')

                if (Path(rebirthdir / 'Rebirth.exe').is_file()):
                    self.gameDirRebirthPicker.RemoveWarning('wrongdir')
                else:
                    self.gameDirRebirthPicker.AddWarning('wrongdir', f'The directory "{rebirthdir}" doesn\'t seem to have a Rebirth installation.')

            else:
                self.gameDirRebirthPicker.AddError('exists', f'The directory "{rebirthdir}" does not exist.')
        else:
            self.gameDirRebirthPicker.ClearErrors()

        if isRelativeDir:
            if bindsdir := self.bindsDirText.GetValue():
                self.bindsDirText.RemoveError('empty')
            else:
                self.bindsDirText.AddError('empty', 'The Binds Directory must contain a name for the binds subdirectory of the Game Directory.  "kb" is the recommended value.')

            if re.search(r'[^0-9a-zA-Z_]', bindsdir):
                self.bindsDirText.AddError('spaces', 'The binds directory name cannot contain spaces or special characters.')
            else:
                self.bindsDirText.RemoveError('spaces')

        else:
            bindsdir = Path(self.bindsDirPicker.GetPath())
            if bindsdir.is_dir():
                self.bindsDirPicker.RemoveError('exists')
            else:
                self.bindsDirPicker.AddError('exists', f'The directory "{bindsdir}" does not exist.')

            if platform.system() == 'Windows':
                if re.search(r'\s+', str(bindsdir)):
                    self.bindsDirPicker.AddError('spaces', 'The binds directory name cannot contain spaces.')
                else:
                    self.bindsDirPicker.RemoveError('spaces')

        profiledir = Path(self.ProfileDirPicker.GetPath())
        if profiledir.is_dir():
            self.ProfileDirPicker.RemoveError('exists')
        else:
            self.ProfileDirPicker.AddError('exists', f'The directory "{profiledir}" does not exist.')

        if evt: evt.Skip()

    def OnGameBindsDirPickerChanged(self, _ = None) -> None:
        if gbdp := self.gameBindsDirPicker:
            path = gbdp.GetValue()
            if re.search(r'\s+', path):
                gbdp.AddError('spaces', 'The game binds directory cannot contain spaces.  Please check "Help > Getting Started with BindControl" for more information.')
            else:
                gbdp.RemoveError('spaces')

            if len(path) > 12:
                gbdp.AddWarning('length', 'This game binds directory is pretty long.  You should try to keep it as short as possible for best results.')
            else:
                gbdp.RemoveWarning('length')

            winpath = PureWindowsPath(path)
            if not winpath.is_absolute():
                gbdp.AddError('absolute', 'The game binds directory must be a valid Windows path, including the drive letter.')
            else:
                gbdp.RemoveError('absolute')

    def OnCBLabelClick(self, evt) -> None:
        cblabel = evt.EventObject
        cblabel.CB.SetValue(not cblabel.CB.IsChecked())
        evt.Skip()

    def ShowAndUpdatePrefs(self) -> None:
        self.ResetKey.CheckConflicts() # Hmm
        if self.ShowModal() == wx.ID_OK:
            config = wx.ConfigBase.Get()

            # check if we changed either GameDir so we know whether to force PopmenuEditor to reload itself
            changedGameDir = False
            if self.gameDirPicker.GetPath()        != config.Read('GamePath')       : changedGameDir = True
            if self.gameDirRebirthPicker.GetPath() != config.Read('GameRebirthPath'): changedGameDir = True

            # Ditto check if reset key changed
            changedResetKey = (self.ResetKey.GetLabel() != config.Read('ResetKey'))

            changedVerboseCustomBinds = (self.VerboseCustomBinds.GetValue() != config.ReadBool('VerboseCustomBinds'))

            ###
            config.WriteBool('RelativeBindsDir', self.gameDirInsideRB.GetValue())
            config.Write('GamePath', self.gameDirPicker.GetPath())
            config.Write('GameRebirthPath', self.gameDirRebirthPicker.GetPath())

            config.Write('GameLang', self.gameLangPicker.GetStringSelection())
            config.Write('BindPath', self.bindsDirPicker.GetPath())
            config.Write('BindTextPath', self.bindsDirText.GetValue())
            if self.gameBindsDirPicker:
                config.Write('GameBindPath', self.gameBindsDirPicker.GetValue())
            config.WriteBool('UseSplitModKeys', self.UseSplitModKeys.GetValue())
            config.WriteBool('FlushAllBinds', self.FlushAllBinds.GetValue())

            config.Write('ResetKey', self.ResetKey.GetLabel())

            config.WriteBool('StartWithLastProfile', self.StartWithLastProfile.GetValue())
            config.Write('ProfilePath', self.ProfileDirPicker.GetPath())

            config.WriteBool('SaveSizeAndPosition', self.SaveSizeAndPosition.GetValue())

            config.Write('ControllerMod1', self.ControllerModPicker1.GetStringSelection())
            config.Write('ControllerMod2', self.ControllerModPicker2.GetStringSelection())
            config.Write('ExtraMod1', self.ExtraModPicker1.GetStringSelection())
            config.Write('ExtraMod2', self.ExtraModPicker2.GetStringSelection())
            config.Write('ExtraMod3', self.ExtraModPicker3.GetStringSelection())
            config.Write('ExtraMod4', self.ExtraModPicker4.GetStringSelection())

            config.WriteBool('VerboseBLF', self.VerboseBLF.GetValue())
            config.WriteBool('CrashOnProfileError', self.CrashOnProfileError.GetValue())
            config.WriteBool('CrashOnBindError', self.CrashOnBindError.GetValue())
            config.WriteBool('VerboseCustomBinds', self.VerboseCustomBinds.GetValue())
            config.WriteBool('ShowInspector', self.ShowInspector.GetValue())
            config.WriteBool('ShowDebugMessages', self.ShowDebugMessages.GetValue())

            config.Flush()

            pub.sendMessage('prefschanged')
            if changedGameDir:
                pub.sendMessage('prefschanged.gamedir')
            if changedResetKey:
                pub.sendMessage('prefschanged.resetkey')
            if changedVerboseCustomBinds:
                pub.sendMessage('prefschanged.verbosebinds')

class controllerModPicker(wx.Choice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
