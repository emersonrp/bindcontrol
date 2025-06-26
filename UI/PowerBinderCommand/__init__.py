import wx

########### Power Binder Command Objects
class PowerBinderCommand():
    Menu = ''
    Name = ''
    def __init__(self, dialog, init = {}):
        self.UI = self.BuildUI(dialog)
        self.Profile = wx.App.Get().Main.Profile
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

commandClasses = {}
commandRevClasses = {}
