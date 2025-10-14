import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Power Unqueue
class PowerUnqueueCmd(PowerBinderCommand):
    Name = "Power Unqueue / Abort"
    Menu = "Powers"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.UnqueueOrAbort = wx.Choice(dialog, choices = ['Unqueue', 'Abort'])
        self.UnqueueOrAbort.SetToolTip('"Unqueue" cancels any queued power, "Abort" also cancels any autopower')
        self.UnqueueOrAbort.SetSelection(0)
        sizer.Add(self.UnqueueOrAbort, 1, wx.ALIGN_CENTER_VERTICAL)

        CenteringSizer.Add(sizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self) -> str:
        if self.UnqueueOrAbort.GetString(self.UnqueueOrAbort.GetSelection()) == 'Unqueue':
            return 'powexecunqueue' if self.Profile.Server() == "Homecoming" else 'px_uq'
        else:
            return 'powexecabort' if self.Profile.Server() == "Homecoming" else 'px_ab'

    def Serialize(self) -> dict:
        return {
            'unqueueorabort' : self.UnqueueOrAbort.GetString(self.UnqueueOrAbort.GetSelection())
        }

    def Deserialize(self, init) -> None:
        self.UnqueueOrAbort.SetStringSelection(init.get('unqueueorabort', 'Unqueue'))

