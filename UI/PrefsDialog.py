import wx
import wx.lib.stattext as ST
import UI
from UI.KeySelectDialog import bcKeyButton
from pathlib import Path

class PrefsDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title = "Preferences")

        config = wx.ConfigBase.Get()

        paddingSizer = wx.BoxSizer(wx.VERTICAL)

        sizer = wx.FlexGridSizer(2,0,0)

        sizer.Add( wx.StaticText(self, label = 'Base Binds Directory:') , 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.bindsDirPicker = wx.DirPickerCtrl(self, path = config.Read('BindPath'))
        self.bindsDirPicker.SetToolTip('Bind files will be written to this folder, inside a profile-specific subfolder.  Keeping this path as short as possible is strongly recommended.')
        sizer.Add( self.bindsDirPicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        self.gameBindsDirPicker = None
        if (wx.Platform != '__WXMSW__'):
            sizer.Add( wx.StaticText(self, label = "In-Game Binds Directory:") , 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
            self.gameBindsDirPicker = wx.TextCtrl(self, value = config.Read('GameBindPath'))
            self.gameBindsDirPicker.SetToolTip('When playing via Wine, the game\'s file paths will be different than the native ones.  Put a Windows path into this box that describes where Wine will find the above directory.  Keeping this path as short as possible is strongly recommended.')
            sizer.Add( self.gameBindsDirPicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        sizer.Add( wx.StaticText(self, label = "Binds Reset Key:"), 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)
        self.ResetKey = bcKeyButton(self, -1, init ={ 'CtlName': 'ResetKey', })
        self.ResetKey.SetLabel( config.Read('ResetKey') )
        self.ResetKey.Profile = None # to appease CheckConflict()
        UI.Labels.update({ 'ResetKey': 'Binds Reset Key'})
        sizer.Add( self.ResetKey, 1, wx.ALL|wx.ALIGN_CENTRE_VERTICAL, 6)


        splitKeyLabel = ST.GenStaticText(self, label = "Bind left and right modifier keys separately:")
        sizer.Add( splitKeyLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.UseSplitModKeys = wx.CheckBox(self)
        self.UseSplitModKeys.SetValue(config.ReadBool('UseSplitModKeys'))
        self.UseSplitModKeys.SetToolTip("By default, BindControl will bind modifier keys, eg CTRL and SHIFT, without regard to which side of the keyboard they're on.  Check this if you'd like to bind the left-side modifier keys separately from the right-side ones.")
        sizer.Add( self.UseSplitModKeys, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        splitKeyLabel.CB = self.UseSplitModKeys
        splitKeyLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )


        flushBindsLabel = ST.GenStaticText(self, label = "Set all binds to default before reapplying:")
        sizer.Add( flushBindsLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6 )
        self.FlushAllBinds = wx.CheckBox(self)
        self.FlushAllBinds.SetValue(config.ReadBool('FlushAllBinds'))
        self.FlushAllBinds.SetToolTip("Set all binds to City of Heroes' default before applying BindControl's binds.  Uncheck this if you have added any binds into the game that are not managed by BindControl.")
        sizer.Add( self.FlushAllBinds, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6 )

        flushBindsLabel.CB = self.FlushAllBinds
        flushBindsLabel.Bind( wx.EVT_LEFT_DOWN, self.onCBLabelClick )

        buttonSizer = wx.StdDialogButtonSizer()
        buttonSizer.AddButton(wx.Button(self, wx.ID_OK))
        buttonSizer.AddButton(wx.Button(self, wx.ID_CANCEL))
        buttonSizer.Realize()

        paddingSizer.Add(sizer, 0, wx.ALL, 10)
        paddingSizer.Add(buttonSizer, 0, wx.ALL|wx.EXPAND, 10)

        self.SetSizerAndFit(paddingSizer)


    def onCBLabelClick(self, evt):
        cblabel = evt.EventObject
        cblabel.CB.SetValue(not cblabel.CB.IsChecked())
        evt.Skip()
