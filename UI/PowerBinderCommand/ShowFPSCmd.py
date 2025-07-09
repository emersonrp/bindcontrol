
import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Window Save / Load
class ShowFPSCmd(PowerBinderCommand):
    Name = "Show FPS etc"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog):
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(wx.StaticText(dialog, wx.ID_ANY, "Show FPS"), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.FPSChoice = wx.Choice(dialog, wx.ID_ANY, choices = ['0', '1', '2', '3', 'Off'])
        self.FPSChoice.SetSelection(4)
        self.FPSChoice.Bind(wx.EVT_CHOICE, self.OnFPSChoice)
        sizer.Add(self.FPSChoice, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        CenteringSizer.Add(sizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        # This is an ugly little dance we do to make sure the StaticText isn't all shrunk horizontally
        dialogwidth = dialog.GetClientRect()[2]
        self.FPSExplanation = wx.StaticText(dialog, wx.ID_ANY, size = wx.Size(dialogwidth, -1),
                                            style = wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        CenteringSizer.Add(self.FPSExplanation, 1, wx.EXPAND)
        self.OnFPSChoice()
        return CenteringSizer

    def MakeBindString(self):
        sel = self.FPSChoice.GetSelection()
        if sel == 4:
            return "-setfps"
        else:
            return f'setfps {sel}'

    def Serialize(self):
        return {
            'fpschoice' : self.FPSChoice.GetSelection(),
        }

    def Deserialize(self, init):
        self.FPSChoice.SetSelection(init.get('fpschoice', 0))
        self.OnFPSChoice()

    def OnFPSChoice(self, evt = None):
        if evt: evt.Skip()
        choice = self.FPSChoice.GetSelection()
        explanation = [
            "Display the camera's POS and PYR coordinates",
            "Display only the FPS",
            "Display the CAM POS and PYR under the FPS",
            "Display the CAM POS and PYR in large type at the left of the screen.",
            "Disable the FPS display",
        ][choice]
        self.FPSExplanation.SetLabel(explanation)
