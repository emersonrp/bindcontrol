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
            'Enable'               : 1,
            'Message'              : "afk Typing Message",
            'StartChat'            : 'ENTER',
            'SlashChat'            : '/',
            'StartEmote'           : ';',
            'AutoReply'            : 'BACKSPACE',
            'TellTarget'           : 'COMMA',
            'QuickChat'            : "'",
            'TypingNotifierEnable' : 1,
            'TypingNotifier'       : '',
        }

        self.Typingnotifierlimit = { 'cmdlist': ["Away From Keyboard","Emote"] }

    def FillTab(self):

        topSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = ControlGroup(self, self, 'Chat Binds')

        sizer.AddLabeledControl(
            ctlName   = 'Enable',
            ctlType = 'checkbox',
            tooltip = 'Enable / Disable chat binds',
        )
        for b in (
            ['StartChat',  'Activates the Chat bar'],
            ['SlashChat',  'Activates the Chat bar with a slash already typed'],
            ['StartEmote', 'Activates the Chat bar with "/em" already typed'],
            ['AutoReply',  'AutoReplies to incoming tells'],
            ['TellTarget', 'Starts a /tell to your current target'],
            ['QuickChat',  'Activates QuickChat'],
        ):
            sizer.AddLabeledControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )
        sizer.AddLabeledControl(
            ctlName = 'TypingNotifierEnable',
            ctlType = 'checkbox',
            tooltip = "Check this to enable the Typing Notifier",
        )
        sizer.AddLabeledControl(
            ctlName = 'TypingNotifier',
            ctlType = 'text',
            tooltip = "Choose the message to display when you are typing chat messages or commands",
        )

        topSizer.Add(sizer)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizer(paddingSizer)
        self.TabTitle = 'Typing Message'
        return self

    def PopulateBindfiles(self):
        profile   = shift.Profile
        ResetFile = profile.ResetFile
        Typing    = self.State

        Notifier = Typing['TypingNotifier']
        if Notifier:
            Notifier = "\\Notifier"

        ResetFile.SetBind(Typing['StartChat'], 'show chatstartchat' . Notifier)
        ResetFile.SetBind(Typing['SlashChat'], 'show chatslashchat' . Notifier)
        ResetFile.SetBind(Typing['StartEmote'],'show chatem ' . Notifier)
        ResetFile.SetBind(Typing['AutoReply'], 'autoreply' . Notifier)
        ResetFile.SetBind(Typing['TellTarget'],'show chatbeginchat /tell target, ' . Notifier)
        ResetFile.SetBind(Typing['QuickChat'], 'quickchat' . Notifier)

    def findconflicts(self, profile):
        Utility.CheckConflict(profile.Typing,"StartChat", "Start Chat Key")
        Utility.CheckConflict(profile.Typing,"SlashChat", "Slashchat Key")
        Utility.CheckConflict(profile.Typing,"StartEmote","Emote Key")
        Utility.CheckConflict(profile.Typing,"AutoReply", "Autoreply Key")
        Utility.CheckConflict(profile.Typing,"TellTarget","Tell Target Key")
        Utility.CheckConflict(profile.Typing,"QuickChat", "Quickchat Key")

    def bindisused(self, profile):
        if getattr(profile, 'Typing', None):
            return profile.Typing['enable']


    UI.Labels.update({
        'Enable' : 'Enable Chat Binds',
        'Message' : '"afk typing" message',
        'StartChat' : 'Start Chat (no "/")',
        'SlashChat' : 'Start Chat (with "/")',
        'StartEmote' : 'Begin emote (types "/em")',
        'AutoReply' : 'AutoReply to incoming /tell',
        'TellTarget' : 'Send /tell to current target',
        'QuickChat' : 'QuickChat',
        'TypingNotifierEnable' : 'Enable Typing Notifier',
        'TypingNotifier' : 'Typing Notifier',
    })
