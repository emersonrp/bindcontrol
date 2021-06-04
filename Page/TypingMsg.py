import wx
from Page import Page
from UI.ControlGroup import ControlGroup

class TypingMsg(Page):

    def __init__(self, parent):
        Page.__init__(self, parent)
        self.TabTitle = "Typing"
        self.Labels = {
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
        }

        self.Typingnotifierlimit = { 'cmdlist': ["Away From Keyboard","Emote"] }

    def InitKeys(self, profile):
        if not getattr(profile, "Typing", None):
            profile.PageState[self] = {
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

    def FillTab(self):

        topSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = ControlGroup(self, 'Chat Binds')

        sizer.AddLabeledControl(
            value   = 'Enable',
            ctltype = 'checkbox',
            module  = self,
            parent  = self,
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
                value = b[0],
                ctltype = 'keybutton',
                module = self,
                parent = self,
                tooltip = b[1],
            )
        sizer.AddLabeledControl(
            value = 'TypingNotifierEnable',
            ctltype = 'checkbox',
            module = self,
            parent = self,
            tooltip = "Check this to enable the Typing Notifier",
        )
        sizer.AddLabeledControl(
            value = 'TypingNotifier',
            ctltype = 'text',
            module = self,
            parent = self,
            tooltip = "Choose the message to display when you are typing chat messages or commands",
        )

        topSizer.Add(sizer)
        self.SetSizer(topSizer)
        self.TabTitle = 'Typing Message'
        return self

    def PopulateBindfiles(self):
        profile   = shift.Profile
        ResetFile = profile.General['ResetFile']
        Typing    = profile.Typing

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
        cbCheckConflict(profile.Typing,"StartChat", "Start Chat Key")
        cbCheckConflict(profile.Typing,"SlashChat", "Slashchat Key")
        cbCheckConflict(profile.Typing,"StartEmote","Emote Key")
        cbCheckConflict(profile.Typing,"AutoReply", "Autoreply Key")
        cbCheckConflict(profile.Typing,"TellTarget","Tell Target Key")
        cbCheckConflict(profile.Typing,"QuickChat", "Quickchat Key")

    def bindisused(self, profile):
        if getattr(profile, 'Typing', None):
            return profile.Typing['enable']

