import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Away From Keyboard
class AFKCmd(PowerBinderCommand):
    Name = "Away From Keyboard"
    Menu = "Social"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AFKName = wx.TextCtrl(dialog, -1)
        self.AFKName.SetHint('Away From Keyboard Text ("AFK" is default)')
        sizer.Add(self.AFKName, 1, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self) -> str:
        message = self.AFKName.GetValue()
        return f"afk {message}" if message else "afk"

    def Serialize(self) -> dict:
        return {'message': self.AFKName.GetValue()}

    def Deserialize(self, init) -> None:
        if 'message' in init:
            self.AFKName.SetValue(init['message'])
