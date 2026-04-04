import wx
from UI.PowerBinder import commandRevClasses

########### Power Binder Command Objects
class PowerBinderCommand:
    Menu = ''
    Name = ''
    UseEditDialog = True

    def __init__(self, dialog, init : dict|None = None) -> None:
        self.Dialog  = dialog
        self.Profile = dialog.Profile
        self.EditDialog = None

        if self.UseEditDialog:
            self.EditDialog = PowerBinderEditDialog(self, dialog)
            self.EditDialog.AddContents(self.BuildUI(self.EditDialog))

        self.State = {}
        if init:
            self.Deserialize(init)
            self.State = init

    # Methods to override
    def BuildUI(self, dialog)   -> wx.Sizer|None : return None
    def MakeBindString(self)    -> str           : return ''
    def Serialize(self)         -> dict          : return {}
    def Deserialize(self, init) -> None          : return
    def OKToClose(self)         -> bool          : return True

    def MakeListEntryString(self) -> str:
        bindstr = self.MakeBindString()
        short_bindstr = "{:.40}{}".format(bindstr, "…" if len(bindstr) > 40 else "")
        return f"{self.Name} - {short_bindstr}"

    def ShowEditDialog(self, callback = None, data = None) -> None:
        if self.EditDialog:
            self.EditDialog.SetTitle(f'Editing Command "{commandRevClasses[type(self)]}"')
            self.EditDialog.Callback = callback
            self.EditDialog.Data     = data

            self.EditDialog.Show()
            self.EditDialog.Raise()

class PowerBinderEditDialog(wx.Dialog):
    def __init__(self, pbc, dialog) -> None:
        super().__init__(dialog, title = "Edit Command", style = wx.DEFAULT_DIALOG_STYLE)

        outerSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.SetMinSize(wx.Size(500, 150))

        self.Page = dialog.Page
        self.PowerBinderCommand = pbc
        self.Callback = None
        self.Data = None

        self.mainSizer.Add(
            self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL),
            0, wx.EXPAND|wx.ALL, 10)

        okbutton = self.FindWindow(wx.ID_OK)
        okbutton.Bind(wx.EVT_BUTTON, self.onOKButton)

        cancelbutton = self.FindWindow(wx.ID_CANCEL)
        cancelbutton.Bind(wx.EVT_BUTTON, self.onCancelButton)

        outerSizer.Add(self.mainSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 3)

        self.SetSizerAndFit(outerSizer)

    def onOKButton(self, evt) -> None:
        pbc = self.PowerBinderCommand
        if pbc.OKToClose():
            evt.Skip()
            pbc.State = pbc.Serialize()
            if self.Callback:
                self.Callback(self.PowerBinderCommand, self.Data)

    def onCancelButton(self,evt) -> None:
        evt.Skip()
        self.PowerBinderCommand.Deserialize(self.PowerBinderCommand.State)
        self.PowerBinderCommand.Dialog.UpdateBindStringDisplay()

    def AddContents(self, contents) -> None:
        self.mainSizer.Insert(0, contents, 1, wx.EXPAND|wx.ALL, 10)
        self.Fit()
        self.Layout()
