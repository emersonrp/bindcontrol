import wx
import UI
import Utility

from Page import Page
from UI.ControlGroup import ControlGroup

class TypingMsg(Page):

    def __init__(self, parent):
        Page.__init__(self, parent)
        self.TabTitle = "Typing"
        self.Init = {
        }

        self.Typingnotifierlimit = { 'cmdlist': ["Away From Keyboard","Emote"] }

    def BuildPage(self):

        topSizer = wx.BoxSizer(wx.VERTICAL)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizer(paddingSizer)
        self.TabTitle = 'Typing Message'
        return self

    def PopulateBindfiles(self):

    def findconflicts(self, profile):

    def bindisused(self, profile):
        if getattr(profile, 'Typing', None):
            return profile.Typing['enable']


    UI.Labels.update({
    })
