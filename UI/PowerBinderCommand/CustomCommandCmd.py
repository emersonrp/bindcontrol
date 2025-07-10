import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Custom Bind
class CustomCommandCmd(PowerBinderCommand):
    Name = "Custom Command"
    # Menu = '' # This one gets treated specially, and should NOT define Menu

    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.customBindName = wx.TextCtrl(dialog, -1)
        self.customBindName.SetHint('Custom Command Text')
        sizer.Add(self.customBindName, 1, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self):
        return self.customBindName.GetValue()

    # We used to call these "Custom Binds" and we're gonna leave them called that
    # in the serialize / deserialize steps just so we don't have to legacy that name.
    def Serialize(self):
        return { 'customBindName': self.customBindName.GetValue() }

    def Deserialize(self,init):
        if init.get('customBindName', ''): self.customBindName.SetValue(init['customBindName'])
