import wx
import wx.adv
from UI.PowerBinderCommand import PowerBinderCommand

####### Custom Bind
class CustomCommandCmd(PowerBinderCommand):
    Name = "Custom Command"
    # Menu = '' # This one gets treated specially, and should NOT define Menu

    def BuildUI(self, dialog) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.customBindName = wx.TextCtrl(dialog, -1)
        self.customBindName.SetHint('Custom Command Text')
        sizer.Add(self.customBindName, 0, wx.EXPAND)

        payload = 'https://wiki.cityofheroesrebirth.com/wiki/List_of_Slash_Commands' if self.Profile.Server() == 'Rebirth' else 'https://homecoming.wiki/wiki/List_of_Slash_Commands'
        link = wx.adv.HyperlinkCtrl(dialog,
            label = 'List of Slash Commands',
            url = payload,
        )
        sizer.Add(link, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 24)

        return sizer

    def HandleLinkClicked(self, evt) -> None:
        linkinfo = evt.GetLinkInfo()
        page = linkinfo.GetHref()
        wx.LaunchDefaultBrowser(page)

    def MakeBindString(self) -> str:
        return self.customBindName.GetValue()

    # We used to call these "Custom Binds" and we're gonna leave them called that
    # in the serialize / deserialize steps just so we don't have to legacy that name.
    def Serialize(self) -> dict:
        return { 'customBindName': self.customBindName.GetValue() }

    def Deserialize(self,init) -> None:
        if init.get('customBindName', ''): self.customBindName.SetValue(init['customBindName'])
