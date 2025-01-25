import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Custom Bind
class CustomBindCmd(PowerBinderCommand):
    Name = "Custom Bind"
    # Menu = '' # This one gets treated specially, and should NOT define Menu

    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.customBindName = wx.TextCtrl(dialog, -1)
        self.customBindName.SetHint('Custom Bind Text')
        sizer.Add(self.customBindName, 1, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self):
        return self.customBindName.GetValue()

    def Serialize(self):
        return { 'customBindName': self.customBindName.GetValue() }

    def Deserialize(self,init):
        if init.get('customBindName', ''): self.customBindName.SetValue(init['customBindName'])
