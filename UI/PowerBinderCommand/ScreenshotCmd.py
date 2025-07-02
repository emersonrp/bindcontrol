import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Screenshot
class ScreenshotCmd(PowerBinderCommand):
    Name = "Screenshot"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog):
        ScreenshotSizer = wx.FlexGridSizer(4, 2, 5, 5)
        ScreenshotSizer.AddGrowableCol(1)

        ScreenshotSizer.Add(wx.StaticText(dialog, -1, "Format:"), flag = wx.ALIGN_CENTER_VERTICAL)

        rbSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ScreenshotJPG = wx.RadioButton(dialog, -1, "JPG", style = wx.ALIGN_CENTER_VERTICAL)
        rbSizer.Add(self.ScreenshotJPG, 1)
        self.ScreenshotTGA = wx.RadioButton(dialog, -1, "TGA", style = wx.ALIGN_CENTER_VERTICAL)
        rbSizer.Add(self.ScreenshotTGA, 1)

        ScreenshotSizer.Add(rbSizer, 1, flag = wx.EXPAND)

        ScreenshotSizer.Add(wx.StaticText(dialog, -1, ""))
        self.ScreenshotHideUI = wx.CheckBox(dialog, -1, "Hide UI while taking screenshot")
        ScreenshotSizer.Add(self.ScreenshotHideUI, 1, flag = wx.EXPAND)

        return ScreenshotSizer

    def MakeBindString(self):
        if self.ScreenshotJPG.GetValue():
            command = "screenshot"
        elif self.ScreenshotTGA.GetValue():
            command = "screenshottga"
        else:
            wx.LogWarning('PowerBindCmd "Screenshot" got an impossible value for jpg/tga')
            return ''

        hideUIText = "screenshotui 0$$" if self.ScreenshotHideUI.IsChecked() else ""

        return f"{hideUIText}{command}"

    def Serialize(self):
        if self.ScreenshotTGA.GetValue():
            command = "screenshottga"
        else:
            command = "screenshot"

        return {
            'command' : command,
            "hideui"  : self.ScreenshotHideUI.IsChecked(),
        }

    def Deserialize(self, init):
        command = init.get('command', '')
        if command == 'screenshot':
            self.ScreenshotJPG.SetValue(True)
        elif command == 'screenshottga':
            self.ScreenshotTGA.SetValue(True)

        self.ScreenshotHideUI.SetValue(init.get('hideui', False))

