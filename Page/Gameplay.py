import wx
import UI
from Icon import GetIcon
from Help import HelpButton

from UI.ControlGroup import ControlGroup
from Page import Page

ordinals = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth")

class Gameplay(Page):

    def __init__(self, parent):
        Page.__init__(self, parent)
        self.TabTitle = "Gameplay"
        self.Init = {
            'TPSEnable'   : False,
            'TPSSelMode'  : "Teammates, then pets",
            'TeamSelect1' : '',
            'TeamSelect2' : '',
            'TeamSelect3' : '',
            'TeamSelect4' : '',
            'TeamSelect5' : '',
            'TeamSelect6' : '',
            'TeamSelect7' : '',
            'TeamSelect8' : '',

            'TeamEnable'  : False,
            'SelNextTeam' : '',
            'SelPrevTeam' : '',
            'IncTeamSize' : '',
            'DecTeamSize' : '',
            'IncTeamPos'  : '',
            'DecTeamPos'  : '',
            'TeamReset'   : '',

            'PetEnable'   : False,
            'SelNextPet'  : '',
            'SelPrevPet'  : '',
            'IncPetSize'  : '',
            'DecPetSize'  : '',

            'FPSEnable'       : False,
            'FPSBindKey'      : 'P',
            'NetgraphBindKey' : 'N',

            'ChatEnable' : True,
            'StartChat'  : 'ENTER',
            'SlashChat'  : '/',
            'StartEmote' : ';',
            'AutoReply'  : 'BACKSPACE',
            'TellTarget' : 'COMMA',
            'QuickChat'  : "'",

            'TypingNotifierEnable' : 1,
            'TypingNotifier'       : 'typing',
        }

    def BuildPage(self):
        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)

        ##### Enable TPS Direct Select
        tpsenablesizer = wx.BoxSizer(wx.HORIZONTAL)

        tpsenable = wx.CheckBox( self, -1, 'Enable Team/Pet Select')
        tpsenable.SetToolTip( wx.ToolTip('Check this to enable the Combined Team/Pet Select Binds') )
        tpsenable.Bind(wx.EVT_CHECKBOX, self.OnTPSEnable)
        self.Ctrls['TPSEnable'] = tpsenable
        tpsenable.SetValue(self.Init['TPSEnable'])

        tpshelpbutton = HelpButton(self, 'TPSBinds.html')

        tpsenablesizer.Add(tpsenable, 0, wx.ALIGN_CENTER_VERTICAL)
        tpsenablesizer.Add(tpshelpbutton, wx.ALIGN_RIGHT)

        leftSizer.Add(tpsenablesizer, 0, wx.ALL, 10)

        ##### direct-select keys
        TPSDirectBox = ControlGroup(self, self, 'Combined Team/Pet Select')

        TPSDirectBox.AddControl(
            ctlName = 'TPSSelMode',
            ctlType = 'choice',
            contents = ['Teammates, then pets','Pets, then teammates','Teammates Only','Pets Only'],
            tooltip = 'Choose the order in which teammates and pets are selected with sequential keypresses',
        )
        for selectid in (1,2,3,4,5,6,7,8):
            TPSDirectBox.AddControl(
                ctlName = f"TeamSelect{selectid}",
                ctlType = 'keybutton',
                tooltip = f"Choose the key that will select team member / pet {selectid}",
            )
        leftSizer.Add(TPSDirectBox, 0, wx.EXPAND|wx.ALL, 10)

        ##### Team Select Binds
        teamenablesizer = wx.BoxSizer(wx.HORIZONTAL)
        teamenable = wx.CheckBox( self, -1, 'Enable Team Select')
        teamenable.SetToolTip( wx.ToolTip('Check this to enable the Single Key Team Select Binds') )
        teamenable.Bind(wx.EVT_CHECKBOX, self.OnTeamEnable)
        self.Ctrls['TeamEnable'] = teamenable
        teamenable.SetValue(self.Init['TeamEnable'])

        teamhelpbutton = HelpButton(self, 'TeamSelectBinds.html')

        teamenablesizer.Add(teamenable, 0, wx.ALIGN_CENTER_VERTICAL)
        teamenablesizer.Add(teamhelpbutton, wx.ALIGN_RIGHT)

        leftSizer.Add(teamenablesizer, 0, wx.ALL, 10)

        TeamSelBox = ControlGroup(self, self, 'Team Select')
        for b in (
            ['SelNextTeam', 'Choose the key that will select the next teammate from the currently selected one'],
            ['SelPrevTeam', 'Choose the key that will select the previous teammate from the currently selected one'],
            ['IncTeamSize', 'Choose the key that will increase the size of your teammate rotation'],
            ['DecTeamSize', 'Choose the key that will decrease the size of your teammate rotation'],
            ['IncTeamPos', 'Choose the key that will move you to the next higher slot in the team rotation'],
            ['DecTeamPos', 'Choose the key that will move you to the next lower slot in the team rotation'],
            ['TeamReset', 'Choose the key that will reset your team rotation to solo'],
        ):
            TeamSelBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )
        leftSizer.Add(TeamSelBox, 0, wx.EXPAND|wx.ALL, 10)

        ##### Pet Select Binds
        petenablesizer = wx.BoxSizer(wx.HORIZONTAL)
        petenable = wx.CheckBox( self, -1, 'Enable Pet Select')
        petenable.SetToolTip( wx.ToolTip('Check this to enable the Single Key Pet Select Binds') )
        petenable.Bind(wx.EVT_CHECKBOX, self.OnPetEnable)
        self.Ctrls['PetEnable'] = petenable
        petenable.SetValue(self.Init['PetEnable'])

        pethelpbutton = HelpButton(self, 'PetSelectBinds.html')

        petenablesizer.Add(petenable, 0, wx.ALIGN_CENTER_VERTICAL)
        petenablesizer.Add(pethelpbutton, wx.ALIGN_RIGHT)

        rightSizer.Add(petenablesizer, 0, wx.ALL, 10)


        PetSelBox = ControlGroup(self, self, 'Pet Select')
        for b in (
            ['SelNextPet', 'Choose the key that will select the next pet from the currently selected one'],
            ['SelPrevPet', 'Choose the key that will select the previous pet from the currently selected one'],
            ['IncPetSize', 'Choose the key that will increase the size of your pet/henchman group rotation'],
            ['DecPetSize', 'Choose the key that will decrease the size of your pet/henchman group rotation'],
        ):
            PetSelBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        rightSizer.Add(PetSelBox, 0, wx.EXPAND|wx.ALL, 10)

        ### Enable FPS
        FPSSizer = wx.FlexGridSizer(0,2,10,10)

        fpsenable = wx.CheckBox( self, -1, 'Enable FPS/Netgraph Binds')
        fpsenable.SetToolTip( wx.ToolTip('Check this to enable the FPS Meter and Network Graph Binds') )
        fpsenable.Bind(wx.EVT_CHECKBOX, self.OnFPSEnable)
        self.Ctrls['FPSEnable'] = fpsenable

        fpshelpbutton = HelpButton(self, 'FPSBinds.html')

        FPSSizer.Add(fpsenable, 0, wx.ALIGN_CENTER_VERTICAL)
        FPSSizer.Add(fpshelpbutton, wx.ALIGN_RIGHT, 0)

        rightSizer.Add(FPSSizer, 0, wx.EXPAND|wx.ALL, 10)

        ##### FPS Keys
        controlsBox = ControlGroup(self, self, "FPS / Netgraph")
        controlsBox.AddControl(
            ctlName = 'FPSBindKey',
            ctlType = 'keybutton',
        )
        controlsBox.AddControl(
            ctlName = 'NetgraphBindKey',
            ctlType = 'keybutton',
        )
        rightSizer.Add(controlsBox, 0, wx.EXPAND|wx.ALL, 10)

        ### Enable Chat
        ChatSizer = wx.FlexGridSizer(0,2,10,10)

        chatenable = wx.CheckBox(self, -1, 'Enable Chat Binds')
        chatenable.SetToolTip( wx.ToolTip('Check this to enable the Chat Binds') )
        chatenable.Bind(wx.EVT_CHECKBOX, self.OnChatEnable)
        self.Ctrls['ChatEnable'] = chatenable

        chathelpbutton = HelpButton(self, 'ChatBinds.html')

        ChatSizer.Add(chatenable, 0, wx.ALIGN_CENTER_VERTICAL)
        ChatSizer.Add(chathelpbutton, wx.ALIGN_RIGHT, 0)

        rightSizer.Add(ChatSizer, 0, wx.EXPAND|wx.ALL, 10)

        chatBindBox = ControlGroup(self, self, 'Chat Binds')

        for b in (
            ['StartChat',  'Activates the Chat bar'],
            ['SlashChat',  'Activates the Chat bar with a slash already typed'],
            ['StartEmote', 'Activates the Chat bar with "/em" already typed'],
            ['AutoReply',  'AutoReplies to incoming tells'],
            ['TellTarget', 'Starts a /tell to your current target'],
            ['QuickChat',  'Activates QuickChat'],
        ):
            chatBindBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        chatBindBox.AddControl(
            ctlName = 'TypingNotifierEnable',
            ctlType = 'checkbox',
            tooltip = "Check this to enable the Typing Notifier",
            callback = self.OnTypeEnable,
        )
        chatBindBox.AddControl(
            ctlName = 'TypingNotifier',
            ctlType = 'text',
            tooltip = "Choose the message to display when you are typing chat messages or commands",
        )

        rightSizer.Add(chatBindBox, 0, wx.EXPAND|wx.ALL, 10)

        topSizer.Add(leftSizer, 0, wx.ALL|wx.EXPAND, 10)
        topSizer.Add(rightSizer, 0, wx.ALL|wx.EXPAND, 10)
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizerAndFit(paddingSizer)

        self.SynchronizeUI()

    def getHelpHandler(self, evt): return

    def SynchronizeUI(self):
        self.OnTPSEnable()
        self.OnTeamEnable()
        self.OnPetEnable()
        self.OnFPSEnable()
        self.OnChatEnable()
        self.OnTypeEnable()

    def OnTPSEnable(self, evt = None):
        self.DisableControls(self.GetState('TPSEnable'),
            ['TPSSelMode','TeamSelect1','TeamSelect2','TeamSelect3',
            'TeamSelect4', 'TeamSelect5','TeamSelect6','TeamSelect7',
            'TeamSelect8'])
        if evt: evt.Skip()

    def OnTeamEnable(self, evt = None):
        self.DisableControls(self.GetState('TeamEnable'),
            ['SelNextTeam', 'SelPrevTeam','IncTeamSize', 'DecTeamSize',
            'IncTeamPos', 'DecTeamPos', 'TeamReset'])
        if evt: evt.Skip()

    def OnPetEnable(self, evt = None):
        self.DisableControls(self.GetState('PetEnable'),
            ['SelNextPet', 'SelPrevPet', 'IncPetSize', 'DecPetSize'])
        if evt: evt.Skip()

    def OnFPSEnable(self, evt = None):
        self.DisableControls(self.GetState('FPSEnable'),
            ['FPSBindKey','NetgraphBindKey'])
        if evt: evt.Skip()

    def OnChatEnable(self, evt = None):
        self.DisableControls(self.GetState('ChatEnable'),
            ['StartChat','SlashChat','StartEmote','AutoReply',
             'TellTarget','QuickChat', 'TypingNotifierEnable', 'TypingNotifier'])
        self.OnTypeEnable()
        if evt: evt.Skip()

    def OnTypeEnable(self, evt = None):
        chatenabled = self.GetState('ChatEnable')
        typeenabled = self.GetState('TypingNotifierEnable')
        self.DisableControls(chatenabled and typeenabled, ['TypingNotifier'])
        if evt: evt.Skip()

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile()

        ### FPS/Netgraph
        if self.GetState('FPSEnable'):
            ResetFile.SetBind(self.Ctrls['FPSBindKey']     .MakeFileKeyBind('++showfps++netgraph'))
            ResetFile.SetBind(self.Ctrls['NetgraphBindKey'].MakeFileKeyBind('++netgraph'))

        ### Team / Pet Select
        if self.GetState('TPSEnable'):
            if (self.GetState('TPSSelMode') != "Pets Only"
                    and
                self.GetState('TPSSelMode') != "Teammates Only"):

                selmethod = "teamselect"
                selnummod = 0
                selmethod1 = "petselect"
                selnummod1 = 1
                if (self.GetState('TPSSelMode') == "Pets, then teammates"):
                    selmethod = "petselect"
                    selnummod = 1
                    selmethod1 = "teamselect"
                    selnummod1 = 0
                selresetfile = self.Profile.GetBindFile("teamsel","reset.txt")
                for i in (1,2,3,4,5,6,7,8):
                    selfile = self.Profile.GetBindFile("teamsel",f"sel{i}.txt")
                    ResetFile.   SetBind(self.Ctrls[f"TeamSelect{i}"].MakeFileKeyBind([f"{selmethod} {i - selnummod}", self.Profile.BLF('teamsel',f"sel{i}.txt")]))
                    selresetfile.SetBind(self.Ctrls[f"TeamSelect{i}"].MakeFileKeyBind([f"{selmethod} {i - selnummod}", self.Profile.BLF('teamsel',f"sel{i}.txt")]))
                    for j in (1,2,3,4,5,6,7,8):
                        if (i == j):
                            selfile.SetBind(self.Ctrls[f"TeamSelect{j}"].MakeFileKeyBind([f"{selmethod1} {j - selnummod1}", self.Profile.BLF('teamsel',"reset.txt")]))
                        else:
                            selfile.SetBind(self.Ctrls[f"TeamSelect{j}"].MakeFileKeyBind([f"{selmethod} {j - selnummod}"  , self.Profile.BLF('teamsel',f"sel{j}.txt")]))

            else:
                selmethod = "teamselect"
                selnummod = 0
                if (self.GetState('TPSSelMode') == "Pets Only"):
                    selmethod = "petselect"
                    selnummod = 1
                for i in (1,2,3,4,5,6,7,8):
                    ResetFile.SetBind(self.Ctrls[f'TeamSelect{i}'].MakeFileKeyBind(f"{selmethod} {i - selnummod}"))

            ResetFile = self.Profile.ResetFile()

        ### Chat Binds with notifier, if appropriate
        if self.GetState('ChatEnable'):
            notifier = ''
            if self.GetState('TypingNotifierEnable'):
                notifier = 'afk ' + self.GetState('TypingNotifier')

            ResetFile.SetBind(self.Ctrls['StartChat'] .MakeFileKeyBind([notifier, 'show chat', 'startchat']))
            ResetFile.SetBind(self.Ctrls['SlashChat'] .MakeFileKeyBind([notifier, 'show chat', 'slashchat']))
            ResetFile.SetBind(self.Ctrls['StartEmote'].MakeFileKeyBind([notifier, 'show chatem ' + notifier]))
            ResetFile.SetBind(self.Ctrls['AutoReply'] .MakeFileKeyBind([notifier, 'autoreply']))
            ResetFile.SetBind(self.Ctrls['TellTarget'].MakeFileKeyBind([notifier, 'show chat', 'beginchat /tell $target, ']))
            ResetFile.SetBind(self.Ctrls['QuickChat'] .MakeFileKeyBind([notifier, 'quickchat']))

    UI.Labels.update({
        'TPSSelMode' : "Team / Pet Select Mode",

        'SelNextTeam' : "Select Next Teammate",
        'SelPrevTeam' : "Select Previous Teammate",
        'IncTeamSize' : "Increase Team Size",
        'DecTeamSize' : "Decrease Team Size",
        'IncTeamPos'  : "Increase Team Position",
        'DecTeamPos'  : "Decrease Team Position",
        'TeamReset'   : "Reset Team Rotation",

        'SelNextPet' : "Select Next Pet",
        'SelPrevPet' : "Select Previous Pet",
        'IncPetSize' : "Increase Pet Group Size",
        'DecPetSize' : "Decrease Pet Group Size",

        'FPSBindKey'      : "Toggle FPS Display",
        'NetgraphBindKey' : "Toggle Netgraph Display",

        'StartChat'            : 'Start Chat (no "/")',
        'SlashChat'            : 'Start Chat (with "/")',
        'StartEmote'           : 'Begin emote (types "/em")',
        'AutoReply'            : 'AutoReply to incoming /tell',
        'TellTarget'           : 'Send /tell to current target',
        'QuickChat'            : 'QuickChat',

        'TypingNotifierEnable' : 'Enable Typing Notifier',
        'TypingNotifier'       : 'Typing Notifier',
    })

    for i in range(1,9):
        UI.Labels[f'TeamSelect{i}'] = f"Select {ordinals[i-1]} Team Member / Pet"
