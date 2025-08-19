import wx
from UI.PowerBinder import commandRevClasses

########### Power Binder Command Objects
class PowerBinderCommand():
    Menu = ''
    Name = ''
    def __init__(self, dialog, init = {}):
        self.Profile = wx.App.Get().Main.Profile
        self.EditDialog = PowerBinderEditDialog(dialog)
        self.EditDialog.AddContents(self.BuildUI(self.EditDialog))
        if init: self.Deserialize(init)

    # Methods to override
    def BuildUI(self, dialog) -> wx.Sizer|None : return None
    def MakeBindString(self) -> str            : return ''
    def Serialize(self) -> dict                : return {}
    def Deserialize(self, init)                : return

    def MakeListEntryString(self):
        bindstr = self.MakeBindString()
        short_bindstr = "{:.40}{}".format(bindstr, "…" if len(bindstr) > 40 else "")
        return f"{self.Name} - {short_bindstr}"

    def ShowEditDialog(self):
        self.EditDialog.SetTitle(f'Editing Command "{commandRevClasses[type(self)]}"')

        return self.EditDialog.ShowModal()

class PowerBinderEditDialog(wx.Dialog):
    def __init__(self, dialog):
        super().__init__(dialog, -1, "Edit Command",
           style = wx.DEFAULT_DIALOG_STYLE)

        outerSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.SetMinSize(wx.Size(500, 150))

        self.Page = dialog.Page

        self.mainSizer.Add(
            self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL),
            0, wx.EXPAND|wx.ALL, 10)

        outerSizer.Add(self.mainSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 3)

        self.SetSizerAndFit(outerSizer)

    def AddContents(self, contents):
        self.mainSizer.Insert(0, contents, 1, wx.EXPAND|wx.ALL, 10)
        self.Fit()
        self.Layout()
