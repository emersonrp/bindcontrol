import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Away From Keyboard
class AFKCmd(PowerBinderCommand):
    Name = "Away From Keyboard"
    Menu = "Social"

    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AFKName = wx.TextCtrl(dialog, -1)
        self.AFKName.SetHint('Away From Keyboard Text ("AFK" is default)')
        sizer.Add(self.AFKName, 1, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self):
        message = self.AFKName.GetValue()
        return f"afk {message}" if message else "afk"

    def Serialize(self):
        return {'message': self.AFKName.GetValue()}

    def Deserialize(self, init):
        if init['message']:
            self.AFKName.SetValue(init['message'])
