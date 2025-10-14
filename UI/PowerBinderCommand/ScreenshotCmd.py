import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Screenshot
class ScreenshotCmd(PowerBinderCommand):
    Name = "Screenshot"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        ScreenshotSizer = wx.BoxSizer(wx.VERTICAL)

        rbSizer = wx.BoxSizer(wx.HORIZONTAL)
        rbSizer.Add(wx.StaticText(dialog, label = "Format:"), 0, flag = wx.ALIGN_CENTER_VERTICAL)
        self.ScreenshotJPG = wx.RadioButton(dialog, label = "JPG", style = wx.ALIGN_CENTER_VERTICAL|wx.RB_GROUP)
        rbSizer.Add(self.ScreenshotJPG, 0, flag = wx.ALIGN_CENTER_VERTICAL)
        self.ScreenshotTGA = wx.RadioButton(dialog, label = "TGA", style = wx.ALIGN_CENTER_VERTICAL)
        rbSizer.Add(self.ScreenshotTGA, 0, flag = wx.ALIGN_CENTER_VERTICAL)

        ScreenshotSizer.Add(rbSizer, 1, flag = wx.ALIGN_CENTER_HORIZONTAL)

        self.ScreenshotHideUI = wx.CheckBox(dialog, label = "Hide UI during screenshot")
        ScreenshotSizer.Add(self.ScreenshotHideUI, 1, flag = wx.EXPAND)

        CenteringSizer.Add(ScreenshotSizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self) -> str:
        if self.ScreenshotTGA.GetValue():
            command = "screenshottga"
        else:
            command = "screenshot"

        hideUIText = "screenshotui 0$$" if self.ScreenshotHideUI.IsChecked() else ""

        return f"{hideUIText}{command}"

    def Serialize(self) -> dict:
        if self.ScreenshotTGA.GetValue():
            command = "screenshottga"
        else:
            command = "screenshot"

        return {
            'command' : command,
            "hideui"  : self.ScreenshotHideUI.IsChecked(),
        }

    def Deserialize(self, init) -> None:
        command = init.get('command', '')
        if command == 'screenshot':
            self.ScreenshotJPG.SetValue(True)
        elif command == 'screenshottga':
            self.ScreenshotTGA.SetValue(True)

        self.ScreenshotHideUI.SetValue(init.get('hideui', False))

