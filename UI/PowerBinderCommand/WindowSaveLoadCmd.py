import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Window Save / Load
class WindowSaveLoadCmd(PowerBinderCommand):
    Name = "Window Save / Load"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.CommandChoice = wx.Choice(dialog, choices = [
            "Save Window Settings to Specified File",
            "Load Window Settings from Specified File",
            "Save Window Settings to wdw.txt",
            "Load Window Settings from wdw.txt",
        ])
        self.CommandChoice.SetSelection(0)
        self.CommandChoice.Bind(wx.EVT_CHOICE, self.OnCommandChoice)
        sizer.Add(self.CommandChoice, 0, wx.ALL, 5)

        self.FilePath = wx.TextCtrl(dialog, size = wx.Size(400, -1),
            value = str(self.Profile.GameBindsDir() / 'windows.txt'))
        sizer.Add(self.FilePath, 0, wx.ALL, 5)

        return sizer

    def MakeBindString(self) -> str:
        sel = self.CommandChoice.GetSelection()
        command = ['wdwsavefile', 'wdwloadfile', 'wdwsave', 'wdwload'][sel]
        filename = f' "{self.FilePath.GetValue()}"' if (sel in (0, 1)) else ''
        return f'{command}{filename}'

    def Serialize(self) -> dict:
        return {
            'command' : self.CommandChoice.GetSelection(),
            'filename' : self.FilePath.GetValue(),
        }

    def Deserialize(self, init) -> None:
        self.CommandChoice.SetSelection(init.get('command', 0))
        self.FilePath.SetValue(init.get('filename', ''))
        self.OnCommandChoice()

    def OnCommandChoice(self, _ = None):
        self.FilePath.Enable(self.CommandChoice.GetSelection() in (0,1))

