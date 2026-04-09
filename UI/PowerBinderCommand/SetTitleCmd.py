import wx
import re

import GameData
from UI.PowerBinderCommand import PowerBinderCommand

####### Title
class SetTitleCmd(PowerBinderCommand):
    Name = "Set Title"
    Menu = "Social"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.titleText = wx.StaticText(dialog, label = "Select Title:")
        titleSizer.Add(self.titleText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)

        self.titleName = wx.Button(dialog)
        titleSizer.Add(self.titleName, 1, wx.ALIGN_CENTER_VERTICAL)

        self.BadgeData   = {}

        self.MassageBadgeData()

        self.titleName.Bind(wx.EVT_BUTTON, self.PopupBadgeMenu)

        return titleSizer

    def MakeBindString(self) -> str:
        match = re.search(r'(\d+)$', self.titleName.GetLabel())
        if match.groups():
            return "settitle " + match.groups()[0]
        else:
            return ''

    def Serialize(self) -> dict:
        return {'titleName': self.titleName.GetLabel()}

    def Deserialize(self, init) -> None:
        if init.get('titleName', ''): self.titleName.SetLabel(init['titleName'])

    def PopupBadgeMenu(self, evt):
        self.titleName.PopupMenu(BadgeMenu(self.titleName, self.BadgeData))

    # set up the GameData badge data with alignment-appropriate names
    def MassageBadgeData(self, evt = None):
        if evt: evt.Skip()

        self.BadgeData = {}
        for category, badges in GameData.Badges.items():
            if category not in self.BadgeData:
                self.BadgeData[category] = {}

                acode = {
                    'Hero' : 'H',
                    'Villain' : 'V',
                    'Vigilante' : 'H',
                    'Rogue' : 'H',
                    'Loyalist' : 'H',
                    'Resistance' : 'H',
                }.get(self.Profile.Alignment(), 'H')
                for badgeid, namedata in badges.items():
                    self.BadgeData[category][namedata[acode]] = badgeid


class BadgeMenu(wx.Menu):
    def __init__(self, button, badgedata):
        super().__init__()

        self.Button = button

        for category in sorted(badgedata):
            badgemenu = wx.Menu()
            self.AppendSubMenu(badgemenu, category)
            for name in sorted(badgedata[category]):
                badgeid = badgedata[category][name]
                badgemenu.Append(wx.ID_ANY, f"{name} - {badgeid}")

        self.Bind(wx.EVT_MENU, self.OnMenuSelection)


    def OnMenuSelection(self, evt):
        evt.Skip()
        menuitem = self.FindItemById(evt.GetId())
        label = menuitem.GetItemLabelText()
        self.Button.SetLabel(label)
