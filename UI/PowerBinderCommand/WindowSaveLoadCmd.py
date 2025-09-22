import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Window Save / Load
class WindowSaveLoadCmd(PowerBinderCommand):
    Name = "Window Save / Load"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.CommandChoice = wx.Choice(dialog, -1, choices = ["Save Window Settings", "Load Window Settings"])
        self.CommandChoice.SetSelection(0)
        sizer.Add(self.CommandChoice, 0, wx.ALL, 5)

        self.FilePath = wx.TextCtrl(dialog, -1, size = wx.Size(400, -1),
            value = str(self.Profile.GameBindsDir() / 'windows.txt'))
        sizer.Add(self.FilePath, 0, wx.ALL, 5)

        return sizer

    def MakeBindString(self) -> str:
        command = ['wdwsavefile', 'wdwloadfile'][self.CommandChoice.GetSelection()]
        return f'{command} "{self.FilePath.GetValue()}"'

    def Serialize(self) -> dict:
        return {
            'command' : self.CommandChoice.GetSelection(),
            'filename' : self.FilePath.GetValue(),
        }

    def Deserialize(self, init) -> None:
        self.CommandChoice.SetSelection(init.get('command', 0))
        self.FilePath.SetValue(init.get('filename', ''))
