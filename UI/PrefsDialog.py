import wx
import wx.lib.stattext as ST
import UI
from UI.KeySelectDialog import bcKeyButton
from bcController import bcController

class PrefsDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title = "Preferences")

        config = wx.ConfigBase.Get()

        overallSizer = wx.BoxSizer(wx.VERTICAL)

        controller = bcController()

        notebook = wx.Notebook(self)

        ###
        # GENERAL PANEL
        ###
        generalPanel = wx.Panel(notebook)
        generalSizer = wx.FlexGridSizer(2,0,0)

        generalSizer.Add( wx.StaticText(generalPanel, label = 'Base Binds Directory:') , 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.bindsDirPicker = wx.DirPickerCtrl(generalPanel, path = config.Read('BindPath'))
        self.bindsDirPicker.SetToolTip('Bind files will be written to this folder, inside a profile-specific subfolder.  Keeping this path as short as possible is strongly recommended.')
        generalSizer.Add( self.bindsDirPicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        self.gameBindsDirPicker = None
        if (wx.Platform != '__WXMSW__'):
            generalSizer.Add( wx.StaticText(generalPanel, label = "In-Game Binds Directory:") , 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
            self.gameBindsDirPicker = wx.TextCtrl(generalPanel, value = config.Read('GameBindPath'))
            self.gameBindsDirPicker.SetToolTip('When playing via Wine, the game\'s file paths will be different than the native ones.  Put a Windows path into this box that describes where Wine will find the above directory.  Keeping this path as short as possible is strongly recommended.')
            generalSizer.Add( self.gameBindsDirPicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        generalSizer.Add( wx.StaticText(generalPanel, label = "Binds Reset Key:"), 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ResetKey = bcKeyButton(generalPanel, -1, init ={ 'CtlName': 'ResetKey', })
        self.ResetKey.SetLabel( config.Read('ResetKey') )
        UI.Labels.update({ 'ResetKey': 'Binds Reset Key'})
        generalSizer.Add( self.ResetKey, 1, wx.ALL|wx.ALIGN_CENTRE_VERTICAL, 6)


        splitKeyLabel = ST.GenStaticText(generalPanel, label = "Bind left and right modifier keys separately:")
        generalSizer.Add( splitKeyLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.UseSplitModKeys = wx.CheckBox(generalPanel)
        self.UseSplitModKeys.SetValue(config.ReadBool('UseSplitModKeys'))
        self.UseSplitModKeys.SetToolTip("By default, BindControl will bind modifier keys, eg CTRL and SHIFT, without regard to which side of the keyboard they're on.  Check this if you'd like to bind the left-side modifier keys separately from the right-side ones.")
        generalSizer.Add( self.UseSplitModKeys, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        setattr(splitKeyLabel, 'CB', self.UseSplitModKeys)
        splitKeyLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        flushBindsLabel = ST.GenStaticText(generalPanel, label = "Reset all binds to default before reapplying:")
        generalSizer.Add( flushBindsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.FlushAllBinds = wx.CheckBox(generalPanel)
        self.FlushAllBinds.SetValue(config.ReadBool('FlushAllBinds'))
        self.FlushAllBinds.SetToolTip("Set all binds to City of Heroes' default before applying BindControl's binds.  Uncheck this if you have added any binds into the game that are not managed by BindControl.")
        generalSizer.Add( self.FlushAllBinds, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        setattr(flushBindsLabel, 'CB', self.FlushAllBinds)
        flushBindsLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        StartWithProfileLabel = wx.StaticText(generalPanel, label = "On startup, start with:")
        generalSizer.Add( StartWithProfileLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        StartWithSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.StartWithNewProfile  = wx.RadioButton(generalPanel, label="New Profile")
        self.StartWithLastProfile = wx.RadioButton(generalPanel, label="Last Profile")
        if config.Read('StartWith') == "New Profile": self.StartWithNewProfile.SetValue(True)
        else:                                         self.StartWithLastProfile.SetValue(True)
        StartWithSizer.Add(self.StartWithNewProfile)
        StartWithSizer.Add(self.StartWithLastProfile)
        generalSizer.Add (StartWithSizer, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        generalPanel.SetSizerAndFit(generalSizer)

        ###
        # CONTROLLER PANEL
        ###
        controllerPanel = wx.Panel(notebook)
        controllerSizer = wx.FlexGridSizer(3,0,0)

        # Controller name display
        controllerNameLabel = ST.GenStaticText(controllerPanel, label = 'Controller:')
        controllerSizer.Add( controllerNameLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        controllerName = ST.GenStaticText(controllerPanel, label = 'No controller detected!')
        if controller.GetNumberJoysticks() > 0:
            controllerName.SetLabel(controller.GetProductName())
        controllerSizer.Add( controllerName, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        controllerSizer.Add( wx.StaticText(controllerPanel, label = ''))

        # Pickers for controller_modifiers
        possible_mods = controller.ListOfPossibleMods()
        controllerModsLabel = ST.GenStaticText(controllerPanel, label = 'Controller Modifiers:')
        controllerSizer.Add( controllerModsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ControllerModPicker1 = controllerModPicker(controllerPanel, choices = possible_mods)
        self.ControllerModPicker1.SetSelection(self.ControllerModPicker1.FindString(config.Read('ControllerMod1')))
        controllerSizer.Add(self.ControllerModPicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.ControllerModPicker2 = controllerModPicker(controllerPanel, choices = possible_mods)
        self.ControllerModPicker2.SetSelection(self.ControllerModPicker2.FindString(config.Read('ControllerMod2')))
        controllerSizer.Add(self.ControllerModPicker2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        # Pickers for extra_modifiers
        extraModsLabel = ST.GenStaticText(controllerPanel, label = 'Extra Modifiers:')
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

        notebook.AddPage(generalPanel, "General", select = True)
        notebook.AddPage(controllerPanel, "Controller")

        buttonSizer = wx.StdDialogButtonSizer()
        buttonSizer.AddButton(wx.Button(self, wx.ID_OK))
        buttonSizer.AddButton(wx.Button(self, wx.ID_CANCEL))
        buttonSizer.Realize()

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(buttonSizer, 0, wx.ALL|wx.EXPAND, 10)

        overallSizer.Add(notebook, 0, wx.ALL|wx.EXPAND)
        overallSizer.Add(paddingSizer, 0, wx.ALL|wx.EXPAND)

        self.SetSizerAndFit(overallSizer)

    def onCBLabelClick(self, evt):
        cblabel = evt.EventObject
        cblabel.CB.SetValue(not cblabel.CB.IsChecked())
        evt.Skip()

class controllerModPicker(wx.Choice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
