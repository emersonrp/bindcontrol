import wx
import wx.html
import webbrowser
from UI.PowerBinderCommand import PowerBinderCommand

####### Custom Bind
class CustomCommandCmd(PowerBinderCommand):
    Name = "Custom Command"
    # Menu = '' # This one gets treated specially, and should NOT define Menu

    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.customBindName = wx.TextCtrl(dialog, -1)
        self.customBindName.SetHint('Custom Command Text')
        sizer.Add(self.customBindName, 0, wx.EXPAND)

        link = wx.html.HtmlWindow(dialog, size = wx.Size(200,40))
        dialog.SetBackgroundColour(link.GetHTMLBackgroundColour())
        payload = 'https://wiki.cityofheroesrebirth.com/wiki/List_of_Slash_Commands' if self.Profile.Server == 'Rebirth' else 'https://homecoming.wiki/wiki/List_of_Slash_Commands'
        link.SetPage(f'<html><body><center><a href="{payload}">List of Slash Commands</a></body></center></html>')
        link.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.HandleLinkClicked)

        sizer.Add(link, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 10)

        return sizer

    def HandleLinkClicked(self, evt):
        linkinfo = evt.GetLinkInfo()
        page = linkinfo.GetHref()
        webbrowser.open(page)

    def MakeBindString(self):
        return self.customBindName.GetValue()

    # We used to call these "Custom Binds" and we're gonna leave them called that
    # in the serialize / deserialize steps just so we don't have to legacy that name.
    def Serialize(self):
        return { 'customBindName': self.customBindName.GetValue() }

    def Deserialize(self,init):
        if init.get('customBindName', ''): self.customBindName.SetValue(init['customBindName'])
