import platform
import re

import wx
import wx.lib.stattext as ST
from pathlib import Path
import UI
from Help import HelpButton
from UI.KeySelectDialog import bcKeyButton
from UI.ControlGroup import cgDirPickerCtrl
from bcController import bcController

class PrefsDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title = "Preferences")

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

        generalSizer.Add( wx.StaticText(generalPanel, label = 'Game Directory:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.gameDirPicker = cgDirPickerCtrl(generalPanel, path = config.Read('GamePath'), size = (300, -1))
        self.gameDirPicker.SetToolTip('This is where your game is installed.  This will be used to install popmenus.')
        self.gameDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.onDirPickerChange)
        generalSizer.Add( self.gameDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        generalSizer.Add( wx.StaticText(generalPanel, label = 'Base Binds Directory:') , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.bindsDirPicker = cgDirPickerCtrl(generalPanel, path = config.Read('BindPath'), size = (300, -1))
        self.bindsDirPicker.SetToolTip('Bind files will be written to this folder, inside a profile-specific subfolder.  Keeping this path as short as possible is strongly recommended.')
        self.bindsDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.onDirPickerChange)
        generalSizer.Add( self.bindsDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        self.gameBindsDirPicker = None
        if (platform.system() != 'Windows'):
            generalSizer.Add( wx.StaticText(generalPanel, label = "In-Game Binds Directory:") , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
            self.gameBindsDirPicker = wx.TextCtrl(generalPanel, value = config.Read('GameBindPath'))
            self.gameBindsDirPicker.SetToolTip('When playing via Wine, the in-game file paths will be different than the native ones.  Put a Windows path into this box that describes where Wine will find the above directory.  Keeping this path as short as possible is strongly recommended.  Check the Manual for more information.')
            generalSizer.Add( self.gameBindsDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        generalSizer.Add( wx.StaticText(generalPanel, label = "Binds Reset Key:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ResetKey = bcKeyButton(generalPanel, -1, init ={ 'CtlName': 'ResetKey', })
        self.ResetKey.SetLabel( config.Read('ResetKey') )
        UI.Labels.update({ 'ResetKey': 'Binds Reset Key'})
        generalSizer.Add( self.ResetKey, 1, wx.ALL|wx.ALIGN_CENTRE_VERTICAL, 6)

        splitKeyLabel = statictextclass(generalPanel, label = "Bind L/R mod keys separately:")
        generalSizer.Add( splitKeyLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.UseSplitModKeys = wx.CheckBox(generalPanel)
        self.UseSplitModKeys.SetValue(config.ReadBool('UseSplitModKeys'))
        self.UseSplitModKeys.SetToolTip("This allows the left and right modifier keys to be bound separately if on the \"right-hand\" side of a bind.  Check the Manual for more information.")
        generalSizer.Add( self.UseSplitModKeys, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        setattr(splitKeyLabel, 'CB', self.UseSplitModKeys)
        splitKeyLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        flushBindsLabel = statictextclass(generalPanel, label = "Set binds to default on reset:")
        generalSizer.Add( flushBindsLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.FlushAllBinds = wx.CheckBox(generalPanel)
        self.FlushAllBinds.SetValue(config.ReadBool('FlushAllBinds'))
        self.FlushAllBinds.SetToolTip("Set all binds to City of Heroes' default before applying BindControl's binds.  Uncheck this if you have added any binds into the game that are not managed by BindControl.")
        generalSizer.Add( self.FlushAllBinds, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        setattr(flushBindsLabel, 'CB', self.FlushAllBinds)
        flushBindsLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        StartWithLastProfileLabel = wx.StaticText(generalPanel, label = "On startup, load last used profile:")
        generalSizer.Add( StartWithLastProfileLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.StartWithLastProfile = wx.CheckBox(generalPanel)
        self.StartWithLastProfile.SetValue(config.ReadBool('StartWithLastProfile'))
        self.StartWithLastProfile.SetToolTip("Load the last profile you were working with when you start the program.")
        generalSizer.Add (self.StartWithLastProfile, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        setattr(StartWithLastProfileLabel, 'CB', self.StartWithLastProfile)
        StartWithLastProfileLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        ProfilePathLabel = wx.StaticText(generalPanel, label = "Path for saved profiles:")
        generalSizer.Add( ProfilePathLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ProfileDirPicker = cgDirPickerCtrl(generalPanel, path = config.Read('ProfilePath'), size = (300, -1))
        self.ProfileDirPicker.SetToolTip('Profiles will be saved to this location.')
        self.ProfileDirPicker.Bind(wx.EVT_DIRPICKER_CHANGED, self.onDirPickerChange)
        generalSizer.Add( self.ProfileDirPicker, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        SaveSizeLabel = statictextclass(generalPanel, label = "Save size / position of window:")
        generalSizer.Add( SaveSizeLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.SaveSizeAndPosition = wx.CheckBox(generalPanel)
        self.SaveSizeAndPosition.SetValue(config.ReadBool('SaveSizeAndPosition'))
        self.SaveSizeAndPosition.SetToolTip("Save the size and position of the BindControl window between sessions.")
        generalSizer.Add( self.SaveSizeAndPosition, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        setattr(SaveSizeLabel, 'CB', self.SaveSizeAndPosition)
        SaveSizeLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        generalPanel.SetSizerAndFit(generalSizer)

        ###
        # CONTROLLER PANEL
        ###
        controllerPanel = wx.Panel(notebook)
        controllerSizer = wx.FlexGridSizer(3,0,0)

        # Controller name display
        controllerNameLabel = statictextclass(controllerPanel, label = 'Controller:')
        controllerSizer.Add( controllerNameLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        controllerName = statictextclass(controllerPanel, label = 'No controller detected!')
        if controller.GetNumberJoysticks() > 0:
            controllerName.SetLabel(controller.GetProductName())
        controllerSizer.Add( controllerName, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        controllerhelpbutton = HelpButton(controllerPanel, 'ControllerModifiers.html')
        controllerSizer.Add( controllerhelpbutton)

        # Pickers for controller_modifiers
        possible_mods = controller.ListOfPossibleMods()
        controllerModsLabel = statictextclass(controllerPanel, label = 'Controller Modifiers:')
        controllerSizer.Add( controllerModsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ControllerModPicker1 = controllerModPicker(controllerPanel, choices = possible_mods)
        self.ControllerModPicker1.SetSelection(self.ControllerModPicker1.FindString(config.Read('ControllerMod1')))
        controllerSizer.Add(self.ControllerModPicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ControllerModPicker2 = controllerModPicker(controllerPanel, choices = possible_mods)
        self.ControllerModPicker2.SetSelection(self.ControllerModPicker2.FindString(config.Read('ControllerMod2')))
        controllerSizer.Add(self.ControllerModPicker2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        # Pickers for extra_modifiers
        extraModsLabel = statictextclass(controllerPanel, label = 'Extra Modifiers:')
        controllerSizer.Add( extraModsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ExtraModPicker1 = controllerModPicker(controllerPanel, choices = possible_mods)
        self.ExtraModPicker1.SetSelection(self.ExtraModPicker1.FindString(config.Read('ExtraMod1')))
        controllerSizer.Add(self.ExtraModPicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ExtraModPicker2 = controllerModPicker(controllerPanel, choices = possible_mods)
        self.ExtraModPicker2.SetSelection(self.ExtraModPicker2.FindString(config.Read('ExtraMod2')))
        controllerSizer.Add(self.ExtraModPicker2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        controllerSizer.Add(wx.StaticText(controllerPanel, label = ''))
        self.ExtraModPicker3 = controllerModPicker(controllerPanel, choices = possible_mods)
        self.ExtraModPicker3.SetSelection(self.ExtraModPicker3.FindString(config.Read('ExtraMod3')))
        controllerSizer.Add(self.ExtraModPicker3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ExtraModPicker4 = controllerModPicker(controllerPanel, choices = possible_mods)
        self.ExtraModPicker4.SetSelection(self.ExtraModPicker4.FindString(config.Read('ExtraMod4')))
        controllerSizer.Add(self.ExtraModPicker4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        controllerPanel.SetSizerAndFit(controllerSizer)

        ###
        # DEBUG PANEL
        ###
        debugPanel = wx.Panel(notebook)
        debugSizer = wx.FlexGridSizer(2,0,0)

        verboseBLFLabel = statictextclass(debugPanel, label = "Verbose in-game feedback when loading bind file:")
        debugSizer.Add( verboseBLFLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.VerboseBLF = wx.CheckBox(debugPanel)
        self.VerboseBLF.SetValue(config.ReadBool('VerboseBLF'))
        tooltip = "Enable output to the chat box whenever a bind file is loaded.  This could be rather spammy, most especially with Speed on Demand binds."
        verboseBLFLabel.SetToolTip(tooltip)
        self.VerboseBLF.SetToolTip(tooltip)
        debugSizer.Add( self.VerboseBLF, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )
        setattr(verboseBLFLabel, 'CB', self.VerboseBLF)
        verboseBLFLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        crashOnBindErrorLabel = statictextclass(debugPanel, label = "Crash on write-binds error:")
        debugSizer.Add( crashOnBindErrorLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.CrashOnBindError = wx.CheckBox(debugPanel)
        self.CrashOnBindError.SetValue(config.ReadBool('CrashOnBindError'))
        tooltip = "Crash and raise a stack trace if there is an error writing the bind files.  You want this turned off unless you are doing deep debugging."
        crashOnBindErrorLabel.SetToolTip(tooltip)
        self.CrashOnBindError.SetToolTip(tooltip)
        debugSizer.Add( self.CrashOnBindError, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )
        setattr(crashOnBindErrorLabel, 'CB', self.CrashOnBindError)
        crashOnBindErrorLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        showInspectorLabel = statictextclass(debugPanel, label = "Show Widget Inspector:")
        debugSizer.Add( showInspectorLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.ShowInspector = wx.CheckBox(debugPanel)
        self.ShowInspector.SetValue(config.ReadBool('ShowInspector'))
        tooltip = "Show the wxPython widget inspector while running.  While harmless, this will open an extra, cryptic window that you're probably not interested in unless debugging."
        showInspectorLabel.SetToolTip(tooltip)
        self.ShowInspector.SetToolTip(tooltip)
        debugSizer.Add( self.ShowInspector, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )
        setattr(showInspectorLabel, 'CB', self.ShowInspector)
        showInspectorLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        showDebugMessagesLabel = statictextclass(debugPanel, label = "Show debug messages in log window.")
        debugSizer.Add( showDebugMessagesLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.ShowDebugMessages = wx.CheckBox(debugPanel)
        self.ShowDebugMessages.SetValue(config.ReadBool('ShowDebugMessages'))
        tooltip = "Show all debug messages in the Log Window.  This is harmless but might be spammy in some circumstances.  If you never look at the log window, you don't need to worry about this."
        showDebugMessagesLabel.SetToolTip(tooltip)
        self.ShowDebugMessages.SetToolTip(tooltip)
        debugSizer.Add( self.ShowDebugMessages, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )
        setattr(showDebugMessagesLabel, 'CB', self.ShowDebugMessages)
        showDebugMessagesLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

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

        self.onDirPickerChange()

    def onDirPickerChange(self, evt = None):
        gamedir = Path(self.gameDirPicker.GetPath())
        if gamedir.is_dir():
            self.gameDirPicker.RemoveError('exists')
            if Path(gamedir / 'bin').is_dir() and Path(gamedir / 'assets').is_dir():
                self.gameDirPicker.RemoveWarning('wrongdir')
            else:
                self.gameDirPicker.AddWarning('wrongdir', f'The directory "{gamedir}" doesn\'t seem to have a Homecoming installation in it.  BindControl only currently supports popmenus with Homecoming installations.  Keybinds will still work.')
        else:
            self.gameDirPicker.AddError('exists', f'The directory "{gamedir}" does not exist.  This is required if you wish to use the popmenu editor.')


        bindsdir = Path(self.bindsDirPicker.GetPath())
        if bindsdir.is_dir():
            self.bindsDirPicker.RemoveError('exists')
        else:
            self.bindsDirPicker.AddError('exists', f'The directory "{bindsdir}" does not exist.')
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


    def onCBLabelClick(self, evt):
        cblabel = evt.EventObject
        cblabel.CB.SetValue(not cblabel.CB.IsChecked())
        evt.Skip()

class controllerModPicker(wx.Choice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
