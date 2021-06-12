import wx
import UI
import Utility
import BindFile
from Utility import BLF

from UI.ControlGroup import ControlGroup
from Page import Page

ordinals = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth")

class Gameplay(Page):

    def __init__(self, parent):
        Page.__init__(self, parent)
        self.TabTitle = "Gameplay"
        self.Init = {
            'FPSEnable': True,
            'FPSBindKey': "P",
            'TPSEnable'   : True,
            'TPSSelMode'  : '',
            'TeamSelect1' : 'UNBOUND',
            'TeamSelect2' : 'UNBOUND',
            'TeamSelect3' : 'UNBOUND',
            'TeamSelect4' : 'UNBOUND',
            'TeamSelect5' : 'UNBOUND',
            'TeamSelect6' : 'UNBOUND',
            'TeamSelect7' : 'UNBOUND',
            'TeamSelect8' : 'UNBOUND',

            'ChatEnable'               : 1,
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

    def BuildPage(self):
        topSizer = wx.BoxSizer(wx.VERTICAL)

        ##### header
        headerSizer = wx.FlexGridSizer(0,2,10,10)

        enablecb = wx.CheckBox( self, -1, 'Enable Team/Pet Select')
        enablecb.SetToolTip( wx.ToolTip('Check this to enable the Team/Pet Select Binds') )
        self.Controls['EnableTeamPetSelectBinds'] = enablecb

        helpbutton = wx.BitmapButton(self, -1, Utility.Icon('Help'))
        helpbutton.Bind(wx.EVT_BUTTON, self.help)

        headerSizer.Add(enablecb, 0, wx.ALIGN_CENTER_VERTICAL)
        headerSizer.Add(helpbutton, wx.ALIGN_RIGHT, 0)

        topSizer.Add(headerSizer)

        ##### direct-select keys
        TPSDirectBox = ControlGroup(self, self, 'Direct Team/Pet Select')

        TPSDirectBox.AddLabeledControl(
            ctlName = 'TPSSelMode',
            ctlType = 'combo',
            contents = ['Teammates, then pets','Pets, then teammates','Teammates Only','Pets Only'],
            tooltip = 'Choose the order in which teammates and pets are selected with sequential keypresses',
        )
        for selectid in (1,2,3,4,5,6,7,8):
            TPSDirectBox.AddLabeledControl(
                ctlName = f"TeamSelect{selectid}",
                ctlType = 'keybutton',
                tooltip = f"Choose the key that will select team member / pet {selectid}",
            )
        topSizer.Add(TPSDirectBox)

        ##### FPS Keys
        controlsBox = ControlGroup(self, self, "FPS / Netgraph")
        controlsBox.AddLabeledControl(
            ctlName = 'FPSEnable',
            ctlType = 'checkbox',
            callback = self.OnFPSEnable,
        )
        controlsBox.AddLabeledControl(
            ctlName = 'FPSBindKey',
            ctlType = 'keybutton',
        )
        topSizer.Add(controlsBox)

        sizer = ControlGroup(self, self, 'Chat Binds')

        sizer.AddLabeledControl(
            ctlName   = 'ChatEnable',
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
        self.SetSizerAndFit(paddingSizer)


    def OnFPSEnable(self, evt):
        self.Controls['FPSBindKey'].Enable(evt.EventObject.IsChecked())

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile()
        ResetFile.SetBind(self.Profile.Gameplay.GetState('FPSBindkey'),'++showfps++netgraph')

        if (self.GetState('TPSSelMode') < 3):
            selmethod = "teamselect"
            selnummod = 0
            selmethod1 = "petselect"
            selnummod1 = 1
            if (self.GetState('TPSSelMode') == 2):
                selmethod = "petselect"
                selnummod = 1
                selmethod1 = "teamselect"
                selnummod1 = 0
            selresetfile = self.Profile.GetBindFile("tps","reset.txt")
            for i in ('1','2','3','4','5','6','7','8'):
                selfile = self.Profile.GetBindFile("tps",f"sel{i}.txt")
                ResetFile.   SetBind(self.GetState(f"TeamSelect{i}"),f"{selmethod} {int(i) - selnummod}" + BLF(self.Profile,'tps',f"sel{i}.txt"))
                selresetfile.SetBind(self.GetState(f"TeamSelect{i}"),f"{selmethod} {int(i) - selnummod}" + BLF(self.Profile,'tps',f"sel{i}.txt"))
                for j in ('1','2','3','4','5','6','7','8'):
                    if (i == j):
                        selfile.SetBind(self.GetState(f"TeamSelect{j}"),f"{selmethod1} {int(j) - selnummod1}" + BLF(self.Profile,'tps',"reset.txt"))
                    else:
                        selfile.SetBind(self.GetState(f"TeamSelect{j}"),f"{selmethod} {int(j) - selnummod}"  + BLF(self.Profile,'tps',"selj.txt"))

        else:
            selmethod = "teamselect"
            selnummod = 0
            if (self.GetState('TPSSelMode') == 4):
                selmethod = "petselect"
                selnummod = 1
            for i in (1,2,3,4,5,6,7,8):
                ResetFile.SetBind(self.GetState('sel1'),"selmethod " + (i - selnummod))

        ResetFile = self.Profile.ResetFile()

        notifier = self.GetState('TypingNotifier')

        # TODO - re-examine the original code, wtf is this
        if notifier:
            notifier = "\\" + notifier

        ResetFile.SetBind(self.GetState('StartChat'), 'show chatstartchat' + notifier)
        ResetFile.SetBind(self.GetState('SlashChat'), 'show chatslashchat' + notifier)
        ResetFile.SetBind(self.GetState('StartEmote'),'show chatem ' + notifier)
        ResetFile.SetBind(self.GetState('AutoReply'), 'autoreply' + notifier)
        ResetFile.SetBind(self.GetState('TellTarget'),'show chatbeginchat /tell target, ' + notifier)
        ResetFile.SetBind(self.GetState('QuickChat'), 'quickchat' + notifier)

    def findconflicts(self):
        Utility.CheckConflict(self,"FPSBindkey","FPS Display Toggle")

        Utility.CheckConflict(self,"StartChat", "Start Chat Key")
        Utility.CheckConflict(self,"SlashChat", "Slashchat Key")
        Utility.CheckConflict(self,"StartEmote","Emote Key")
        Utility.CheckConflict(self,"AutoReply", "Autoreply Key")
        Utility.CheckConflict(self,"TellTarget","Tell Target Key")
        Utility.CheckConflict(self,"QuickChat", "Quickchat Key")

    def bindisused(self):
        return self.GetState('Enable')

    UI.Labels.update({
        'FPSEnable'  : "Enable the FPS/Netgraph bind",
        'FPSBindKey' : "Turn on FPS and Netgraph",

        'ChatEnable' : 'Enable Chat Binds',
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

    for i in range(1,9):
        UI.Labels[f'TeamSelect{i}'] = f"Select {ordinals[i-1]} Team Member / Pet"
