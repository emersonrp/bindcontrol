import platform
import re

import wx
import wx.lib.stattext as ST
from pathlib import Path
from Help import HelpButton
from UI.KeySelectDialog import bcKeyButton
from UI.ControlGroup import cgDirPickerCtrl, cgTextCtrl
from bcController import bcController

class PrefsDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title = "Preferences")

        config = wx.ConfigBase.Get()

        overallSizer = wx.BoxSizer(wx.VERTICAL)

        controller = bcController()

        notebook = wx.Notebook(self)

        statictextclass = wx.StaticText if platform.system() == "Windows" else ST.GenStaticText

        ###
        # GENERAL PANEL
        ###
        generalPanel = wx.Panel(notebook)
        generalSizer = wx.FlexGridSizer(2,0,0)

        generalSizer.Add(wx.StaticText(generalPanel, label = 'Homecoming Game Directory:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.gameDirPicker = cgDirPickerCtrl(generalPanel, path = config.Read('GamePath'), size = (300, -1))
        self.gameDirPicker.DefaultToolTip = 'This is where Homecoming is installed.  This will be used to install popmenus, and is optional.'
        self.gameDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPickerChange)
        generalSizer.Add(self.gameDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        generalSizer.Add(wx.StaticText(generalPanel, label = 'Rebirth Game Directory:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.gameDirRebirthPicker = cgDirPickerCtrl(generalPanel, path = config.Read('GameRebirthPath'), size = (300, -1))
        self.gameDirRebirthPicker.DefaultToolTip = 'This is where Rebirth is installed.  This will be used to install popmenus, and is optional.'
        self.gameDirRebirthPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPickerChange)
        generalSizer.Add(self.gameDirRebirthPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        generalSizer.Add(wx.StaticText(generalPanel, label = 'Game Language:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.gameLangPicker = wx.Choice(generalPanel, choices = ['ChineseTraditional','English','French','German','Japanese','Korean','uk'])
        self.gameLangPicker.SetSelection(self.gameLangPicker.FindString(config.Read('GameLang')))
        self.gameLangPicker.SetToolTip('The language of your installed game.  This is necessary to locate popmenus correctly.')
        generalSizer.Add(self.gameLangPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        generalSizer.Add(wx.StaticText(generalPanel, label = 'Base Binds Directory:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.bindsDirPicker = cgDirPickerCtrl(generalPanel, path = config.Read('BindPath'), size = (300, -1))
        self.bindsDirPicker.DefaultToolTip = 'Bind files will be written to this folder, inside a profile-specific subfolder.  Keeping this path as short as possible is strongly recommended.'
        self.bindsDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPickerChange)
        generalSizer.Add(self.bindsDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        self.gameBindsDirPicker = None
        if (platform.system() != 'Windows'):
            generalSizer.Add(wx.StaticText(generalPanel, label = "In-Game Binds Directory:") , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
            self.gameBindsDirPicker = cgTextCtrl(generalPanel, value = config.Read('GameBindPath'))
            self.gameBindsDirPicker.DefaultToolTip = 'When playing via Wine, the in-game file paths will be different than the native ones.  Put a Windows path into this box that describes where Wine will find the above directory.  Keeping this path as short as possible is strongly recommended.  Check the Manual for more information.'
            self.gameBindsDirPicker.Bind(wx.EVT_TEXT, self.OnGameBindsDirPickerChanged)
            generalSizer.Add(self.gameBindsDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        generalSizer.Add(wx.StaticText(generalPanel, label = "Binds Reset Key:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        resetKey = config.Read('ResetKey')
        self.ResetKey = bcKeyButton(generalPanel, -1, init ={ 'CtlName': 'ResetKey', 'Key' : resetKey })
        self.ResetKey.SetLabel(resetKey)
        self.ResetKey.DefaultToolTip = 'This is the key that will reset your binds to their default state, and stop all movement, if movement binds are installed.'
        generalSizer.Add(self.ResetKey, 1, wx.ALL|wx.ALIGN_CENTRE_VERTICAL, 6)

        splitKeyLabel = statictextclass(generalPanel, label = "Bind L/R mod keys separately:")
        generalSizer.Add(splitKeyLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.UseSplitModKeys = wx.CheckBox(generalPanel)
        self.UseSplitModKeys.SetValue(config.ReadBool('UseSplitModKeys'))
        self.UseSplitModKeys.SetToolTip("This allows the left and right modifier keys to be bound separately if on the \"right-hand\" side of a bind.  Check the Manual for more information.")
        generalSizer.Add(self.UseSplitModKeys, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        setattr(splitKeyLabel, 'CB', self.UseSplitModKeys)
        splitKeyLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        flushBindsLabel = statictextclass(generalPanel, label = "Set binds to default on reset:")
        generalSizer.Add(flushBindsLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.FlushAllBinds = wx.CheckBox(generalPanel)
        self.FlushAllBinds.SetValue(config.ReadBool('FlushAllBinds'))
        self.FlushAllBinds.SetToolTip("Set all binds to City of Heroes' default before applying / resetting BindControl's binds.  Uncheck this if you have added any binds into the game that are not managed by BindControl.")
        generalSizer.Add(self.FlushAllBinds, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        setattr(flushBindsLabel, 'CB', self.FlushAllBinds)
        flushBindsLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        StartWithLastProfileLabel = wx.StaticText(generalPanel, label = "On startup, load last used profile:")
        generalSizer.Add(StartWithLastProfileLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.StartWithLastProfile = wx.CheckBox(generalPanel)
        self.StartWithLastProfile.SetValue(config.ReadBool('StartWithLastProfile'))
        self.StartWithLastProfile.SetToolTip("Load the last profile you were working with when you start the program.")
        generalSizer.Add (self.StartWithLastProfile, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        setattr(StartWithLastProfileLabel, 'CB', self.StartWithLastProfile)
        StartWithLastProfileLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        ProfilePathLabel = wx.StaticText(generalPanel, label = "Path for saved profiles:")
        generalSizer.Add(ProfilePathLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ProfileDirPicker = cgDirPickerCtrl(generalPanel, path = config.Read('ProfilePath'), size = (300, -1))
        self.ProfileDirPicker.SetToolTip('Profiles will be saved to this location.')
        self.ProfileDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPickerChange)
        generalSizer.Add(self.ProfileDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        SaveSizeLabel = statictextclass(generalPanel, label = "Save size / position of window:")
        generalSizer.Add(SaveSizeLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.SaveSizeAndPosition = wx.CheckBox(generalPanel)
        self.SaveSizeAndPosition.SetValue(config.ReadBool('SaveSizeAndPosition'))
        self.SaveSizeAndPosition.SetToolTip("Save the size and position of the BindControl window between sessions.")
        generalSizer.Add(self.SaveSizeAndPosition, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        setattr(SaveSizeLabel, 'CB', self.SaveSizeAndPosition)
        SaveSizeLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        generalPanel.SetSizerAndFit(generalSizer)

        ###
        # CONTROLLER PANEL
        ###
        controllerPanel = wx.Panel(notebook)
        controllerSizer = wx.FlexGridSizer(3,0,0)

        # Controller name display
        controllerNameLabel = statictextclass(controllerPanel, label = 'Controller:')
        controllerSizer.Add(controllerNameLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        controllerName = statictextclass(controllerPanel, label = 'No controller detected!')
        if controller.GetNumberJoysticks() > 0:
            controllerName.SetLabel(controller.GetProductName())
        controllerSizer.Add(controllerName, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        controllerhelpbutton = HelpButton(controllerPanel, 'ControllerModifiers.html')
        controllerSizer.Add(controllerhelpbutton)

        # Pickers for controller_modifiers
        possible_mods = controller.ListOfPossibleMods()
        controllerModsLabel = statictextclass(controllerPanel, label = 'Controller Modifiers:')
        controllerSizer.Add(controllerModsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ControllerModPicker1 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ControllerModPicker1.SetSelection(self.ControllerModPicker1.FindString(config.Read('ControllerMod1')))
        controllerSizer.Add(self.ControllerModPicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ControllerModPicker2 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ControllerModPicker2.SetSelection(self.ControllerModPicker2.FindString(config.Read('ControllerMod2')))
        controllerSizer.Add(self.ControllerModPicker2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        # Pickers for extra_modifiers
        extraModsLabel = statictextclass(controllerPanel, label = 'Extra Modifiers:')
        controllerSizer.Add(extraModsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ExtraModPicker1 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ExtraModPicker1.SetSelection(self.ExtraModPicker1.FindString(config.Read('ExtraMod1')))
        controllerSizer.Add(self.ExtraModPicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ExtraModPicker2 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ExtraModPicker2.SetSelection(self.ExtraModPicker2.FindString(config.Read('ExtraMod2')))
        controllerSizer.Add(self.ExtraModPicker2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        controllerSizer.Add(wx.StaticText(controllerPanel, label = ''))
        self.ExtraModPicker3 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ExtraModPicker3.SetSelection(self.ExtraModPicker3.FindString(config.Read('ExtraMod3')))
        controllerSizer.Add(self.ExtraModPicker3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ExtraModPicker4 = wx.Choice(controllerPanel, choices = possible_mods)
        self.ExtraModPicker4.SetSelection(self.ExtraModPicker4.FindString(config.Read('ExtraMod4')))
        controllerSizer.Add(self.ExtraModPicker4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        controllerPanel.SetSizerAndFit(controllerSizer)

        ###
        # DEBUG PANEL
        ###
        debugPanel = wx.Panel(notebook)
        debugSizer = wx.FlexGridSizer(2,0,0)

        verboseBLFLabel = statictextclass(debugPanel, label = "Verbose in-game feedback when loading bind file:")
        debugSizer.Add(verboseBLFLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.VerboseBLF = wx.CheckBox(debugPanel)
        self.VerboseBLF.SetValue(config.ReadBool('VerboseBLF'))
        tooltip = "Enable output to the chat box whenever a bind file is loaded.  This could be rather spammy, most especially with Speed on Demand binds."
        verboseBLFLabel.SetToolTip(tooltip)
        self.VerboseBLF.SetToolTip(tooltip)
        debugSizer.Add(self.VerboseBLF, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        setattr(verboseBLFLabel, 'CB', self.VerboseBLF)
        verboseBLFLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        crashOnBindErrorLabel = statictextclass(debugPanel, label = "Crash on write-binds error:")
        debugSizer.Add(crashOnBindErrorLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.CrashOnBindError = wx.CheckBox(debugPanel)
        self.CrashOnBindError.SetValue(config.ReadBool('CrashOnBindError'))
        tooltip = "Crash and raise a stack trace if there is an error writing the bind files.  You want this turned off unless you are doing deep debugging."
        crashOnBindErrorLabel.SetToolTip(tooltip)
        self.CrashOnBindError.SetToolTip(tooltip)
        debugSizer.Add(self.CrashOnBindError, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        setattr(crashOnBindErrorLabel, 'CB', self.CrashOnBindError)
        crashOnBindErrorLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        showInspectorLabel = statictextclass(debugPanel, label = "Show Widget Inspector (requires restart):")
        debugSizer.Add(showInspectorLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ShowInspector = wx.CheckBox(debugPanel)
        self.ShowInspector.SetValue(config.ReadBool('ShowInspector'))
        tooltip = "Show the wxPython widget inspector while running.  While harmless, this will open an extra, cryptic window that you're probably not interested in unless debugging."
        showInspectorLabel.SetToolTip(tooltip)
        self.ShowInspector.SetToolTip(tooltip)
        debugSizer.Add(self.ShowInspector, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        setattr(showInspectorLabel, 'CB', self.ShowInspector)
        showInspectorLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        showDebugMessagesLabel = statictextclass(debugPanel, label = "Show debug messages in log window.")
        debugSizer.Add(showDebugMessagesLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ShowDebugMessages = wx.CheckBox(debugPanel)
        self.ShowDebugMessages.SetValue(config.ReadBool('ShowDebugMessages'))
        tooltip = "Show all debug messages in the Log Window.  This is harmless but might be spammy in some circumstances.  If you never look at the log window, you don't need to worry about this."
        showDebugMessagesLabel.SetToolTip(tooltip)
        self.ShowDebugMessages.SetToolTip(tooltip)
        debugSizer.Add(self.ShowDebugMessages, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        setattr(showDebugMessagesLabel, 'CB', self.ShowDebugMessages)
        showDebugMessagesLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        debugPanel.SetSizerAndFit(debugSizer)

        notebook.AddPage(generalPanel, "General", select = True)
        notebook.AddPage(controllerPanel, "Controller")
        notebook.AddPage(debugPanel, "Debug")

        buttonSizer = wx.StdDialogButtonSizer()
        buttonSizer.AddButton(wx.Button(self, wx.ID_OK))
        buttonSizer.AddButton(wx.Button(self, wx.ID_CANCEL))
        buttonSizer.Realize()

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(buttonSizer, 0, wx.ALL|wx.EXPAND, 10)

        overallSizer.Add(notebook, 0, wx.ALL|wx.EXPAND)
        overallSizer.Add(paddingSizer, 0, wx.ALL|wx.EXPAND)

        self.SetSizerAndFit(overallSizer)

        self.OnDirPickerChange()
        self.OnGameBindsDirPickerChanged()

    def OnDirPickerChange(self, evt = None):
        # Check the gamedir picker
        gamedir = Path(self.gameDirPicker.GetPath())
        if gamedir.is_absolute():
            if gamedir.is_dir():
                self.gameDirPicker.RemoveError('exists')

                if ( Path(gamedir / 'bin').is_dir() and Path(gamedir / 'assets').is_dir()):
                    self.gameDirPicker.RemoveWarning('wrongdir')
                else:
                    self.gameDirPicker.AddWarning('wrongdir', f'The directory "{gamedir}" doesn\'t seem to have a Homecoming installation.  BindControl needs this to install popmenus for Homecoming-based Profiles.  Keybinds will still work, and this setting is optional.')

            else:
                self.gameDirPicker.AddError('exists', f'The directory "{gamedir}" does not exist.  This is required if you wish to use the popmenu editor with Homecoming installations, but is otherwise optional.')
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
                    self.gameDirRebirthPicker.AddWarning('wrongdir', f'The directory "{rebirthdir}" doesn\'t seem to have a Rebirth installation.  BindControl needs this to install popmenus for Rebirth-based Profiles.  Keybinds will still work, and this setting is optional.')

            else:
                self.gameDirRebirthPicker.AddError('exists', f'The directory "{rebirthdir}" does not exist.  This is required if you wish to use the popmenu editor with Rebirth installations, but is otherwise optional.')
        else:
            self.gameDirRebirthPicker.ClearErrors()

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

    def OnGameBindsDirPickerChanged(self, _ = None):
        if gbdp := self.gameBindsDirPicker:
            if re.search(r'\s+', gbdp.GetValue()):
                gbdp.AddError('spaces', 'The game binds directory cannot contain spaces.  Please check the manual for more information.')
            else:
                gbdp.RemoveError('spaces')

    def OnCBLabelClick(self, evt):
        cblabel = evt.EventObject
        cblabel.CB.SetValue(not cblabel.CB.IsChecked())
        evt.Skip()

    def ShowAndUpdatePrefs(self):
        if self.ShowModal() == wx.ID_OK:
            config = wx.ConfigBase.Get()
            config.Write('GamePath', self.gameDirPicker.GetPath())
            config.Write('GameRebirthPath', self.gameDirRebirthPicker.GetPath())
            config.Write('GameLang', self.gameLangPicker.GetStringSelection())
            config.Write('BindPath', self.bindsDirPicker.GetPath())
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
            config.WriteBool('CrashOnBindError', self.CrashOnBindError.GetValue())
            config.WriteBool('ShowInspector', self.ShowInspector.GetValue())
            config.WriteBool('ShowDebugMessages', self.ShowDebugMessages.GetValue())

            config.Flush()

            if profile := wx.App.Get().Main.Profile:
                # repopulate the Popmenu Editor, in case we fiddled with GameDir
                profile.PopmenuEditor.SynchronizeUI()

                # and highlight buttons as needed in case we fiddled with ReseyKey
                profile.CheckAllConflicts()

class controllerModPicker(wx.Choice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
