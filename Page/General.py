# UI / logic for the 'general' panel
import wx
import wx.lib.stattext as ST
import UI
from Icon import GetIcon
import GameData

from UI.ControlGroup import ControlGroup
from UI.IncarnateBox import IncarnateBox
# from UI.ChatColorPicker import ChatColorPicker, ChatColors

from Page import Page

class General(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Init = {
            'Alignment' : 'Hero',
            'Origin': "Magic",
            'Archetype': 'Mastermind',
            'Primary': '',
            'Secondary': '',
            'Epic': '',
            'Pool1': '',
            'Pool2': '',
            'Pool3': '',
            'Pool4': '',

            'ChatEnable' : False,
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

        powersBox = ControlGroup(self, self, 'Powers')

        # first the hand-rolled "Profile" + profilename
        ProfileLabel = wx.StaticText(powersBox.GetStaticBox(), -1, "")
        ProfileLabel.SetLabelMarkup("<b>Profile:</b>")
        powersBox.InnerSizer.Add(ProfileLabel, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 6)

        self.nameBox = wx.Panel(powersBox.GetStaticBox())
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.nameBox.SetSizer(nameSizer)

        self.OriginIcon    = wx.StaticBitmap(self.nameBox, size = (32, 32))
        self.NameDisplay   = ST.GenStaticText(self.nameBox, -1, "", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
        self.ArchetypeIcon = wx.StaticBitmap(self.nameBox, size = (32,32))

        self.NameDisplay.SetFont(wx.Font(wx.FontInfo().Bold()))

        nameSizer.Add(self.OriginIcon, 0, wx.ALL, 6)
        nameSizer.Add(self.NameDisplay, 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 6)
        nameSizer.Add(self.ArchetypeIcon, 0, wx.ALL, 6)

        powersBox.InnerSizer.Add(self.nameBox, 1, wx.EXPAND)

        alignmentchoices = []
        for Alignment in GameData.Alignments:
            alignmentchoices.append([Alignment, GetIcon(f"Alignments/{Alignment}")])
        alignmentpicker = powersBox.AddControl(
            ctlName = 'Alignment',
            ctlType  = 'choice',
            contents = GameData.Alignments,
            callback = self.OnPickAlignment,
        )
        alignmentpicker.SetMinSize([200,-1])

        originchoices = []
        for Origin in GameData.Origins:
            originchoices.append([Origin, GetIcon(f"Origins/{Origin}")])
        originpicker = powersBox.AddControl(
            ctlName = 'Origin',
            ctlType = 'choice',
            contents = GameData.Origins,
            callback = self.OnPickOrigin,
        )
        originpicker.SetMinSize([200,-1])

        archchoices = []
        for Arch in sorted(GameData.Archetypes):
            archchoices.append([Arch, GetIcon(f"Archetypes/{Arch}")])
        archpicker = powersBox.AddControl(
            ctlName = 'Archetype',
            ctlType = 'choice',
            contents = sorted(GameData.Archetypes),
            callback = self.OnPickArchetype,
        )
        archpicker.SetMinSize([200,-1])

        powersBox.AddControl(
            ctlName = 'Primary',
            ctlType = 'choice',
            callback = self.OnPickPrimaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Secondary',
            ctlType = 'choice',
            callback = self.OnPickSecondaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Epic',
            ctlType = 'choice',
            callback = self.OnPickEpicPowerSet,
        )
        poolcontents = sorted(GameData.MiscPowers['Pool'])
        poolcontents.insert(0, '')
        powersBox.AddControl(
            ctlName = 'Pool1',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool2',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool3',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool4',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )

        ChatSizer = wx.BoxSizer(wx.VERTICAL)

        # ### Chat Color Picker
        # ChatColorSizer = wx.StaticBoxSizer(wx.VERTICAL, self, "Chat Colors")
        # ChatColorEnable = wx.CheckBox(ChatColorSizer.GetStaticBox(), -1, 'Use Custom Chat Colors')
        # ChatColorEnable.SetToolTip( wx.ToolTip('Check this to select custom colors for your chat messages'))
        # setattr(ChatColorEnable, "CtlName", "ChatColorEnable")
        # self.Ctrls['ChatColorEnable'] = ChatColorEnable
        # ChatColorEnable.Bind(wx.EVT_CHECKBOX, self.OnColorEnable)
        # ChatColors = ChatColorPicker(ChatColorSizer.GetStaticBox(), self, 'Chat', {
        #     'border'     : wx.BLACK,
        #     'background' : wx.WHITE,
        #     'text'       : wx.BLACK,
        # })
        # ChatColorSizer.Add(ChatColorEnable, 0, wx.ALL, 6)
        # ChatColorSizer.Add(ChatColors, 0, wx.ALL, 10)
        # ChatSizer.Add(ChatColorSizer, 0)

        ## Typing Notifier
        TNSizer = wx.StaticBoxSizer(wx.VERTICAL, self, "Typing Notifier")
        TNEnable = wx.CheckBox(TNSizer.GetStaticBox(), -1, 'Use Typing Notifier')
        TNEnable.SetToolTip(
                wx.ToolTip('Check this to enable a floating "typing" notifier when you are typing into the chat box'))
        setattr(TNEnable, "CtlName", 'TypingNotifierEnable')
        TNEnable.Bind(wx.EVT_CHECKBOX, self.OnTypeEnable)
        self.Ctrls['TypingNotifierEnable'] = TNEnable
        TNCtrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        TNLabel = wx.StaticText(TNSizer.GetStaticBox(), label = "Typing Notifier:", style=wx.ALIGN_RIGHT)
        TN = wx.TextCtrl(TNSizer.GetStaticBox(), value = self.Init['TypingNotifier'], style=wx.TE_CENTER)
        setattr(TN, "CtlName", 'TypingNotifier')
        setattr(TN, "CtlLabel", TNLabel)
        self.Ctrls['TypingNotifier'] = TN
        TNCtrlSizer.Add(TNLabel, 1, wx.ALL|wx.ALIGN_CENTER, 6)
        TNCtrlSizer.Add(TN,      1, wx.ALL, 6)

        TNSizer.Add(TNEnable,    0, wx.ALL, 5)
        TNSizer.Add(TNCtrlSizer, 0, wx.ALL|wx.EXPAND, 5)

        ChatSizer.Add(TNSizer, 0, wx.TOP|wx.EXPAND, 6)

        ### Chat binds
        chatBindBox = ControlGroup(self, self, 'Chat Binds')

        for b in (
                # ['StartChat',  'Activates the Chat bar with notifier and custom colors if selected'],
            ['StartChat',  'Activates the Chat bar with notifier if selected'],
            ['SlashChat',  'Activates the Chat bar with notifier and a slash already typed'],
            ['StartEmote', 'Activates the Chat bar with notifier and "/em" already typed'],
            ['AutoReply',  'AutoReplies to incoming tells with notifier'],
            ['TellTarget', 'Starts a /tell to your current target with notifier'],
            ['QuickChat',  'Pops up QuickChat menu, with notifier'],
        ):
            chatBindBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )
        ChatSizer.Add(chatBindBox, 1, wx.EXPAND)

        ### Incarnate interface
        self.IncarnateBox = IncarnateBox(self)

        topSizer.Add(powersBox, 0, wx.RIGHT|wx.EXPAND, 10)
        topSizer.Add(ChatSizer, 0,          wx.EXPAND, 0)

        centeringSizer  = wx.BoxSizer(wx.VERTICAL)
        centeringSizer.Add(topSizer,           0, wx.TOP|wx.EXPAND, 10)
        centeringSizer.Add(self.IncarnateBox,  0, wx.TOP|wx.EXPAND, 6)

        self.MainSizer.Add(centeringSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.SynchronizeUI()

    def SynchronizeUI(self):
        self.OnPickAlignment()
        self.OnPickOrigin()
        self.OnPickArchetype()
        self.OnTypeEnable()
        # self.OnColorEnable()

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile()

        colorstring = ''
        # if self.GetState('ChatColorEnable'):
        #     colorstring = ChatColors(
        #         self.GetState('ChatForeground'),
        #         self.GetState('ChatBackground'),
        #         self.GetState('ChatBorder'),
        #     )

        notifier = ''
        if self.GetState('TypingNotifierEnable'):
            notifier = 'afk ' + self.GetState('TypingNotifier')

        startchatcommand = "startchat "
        # if self.GetState('ChatColorEnable'):
            # startchatcommand = "beginchat "

        ResetFile.SetBind(self.Ctrls['StartChat'] .MakeFileKeyBind([notifier, 'show chat', startchatcommand + colorstring]))
        ResetFile.SetBind(self.Ctrls['SlashChat'] .MakeFileKeyBind([notifier, 'show chat', 'slashchat']))
        ResetFile.SetBind(self.Ctrls['StartEmote'].MakeFileKeyBind([notifier, 'show chatem ' + notifier]))
        ResetFile.SetBind(self.Ctrls['AutoReply'] .MakeFileKeyBind([notifier, 'autoreply']))
        ResetFile.SetBind(self.Ctrls['TellTarget'].MakeFileKeyBind([notifier, 'show chat', 'beginchat /tell $target, ']))
        ResetFile.SetBind(self.Ctrls['QuickChat'] .MakeFileKeyBind([notifier, 'quickchat']))

        return True

    # we only fiddle with ResetFile, which is already taken care of.
    def AllBindFiles(self):
        return {
            'files' : [],
            'dirs'  : [],
        }

    ### EVENT HANDLERS
    def OnPickAlignment(self, evt = None):
        # TODO put this in Gamedata?
        bgcolor = {
            'Hero'       : ( 35, 130, 212),
            'Villain'    : (225,  65,  65),
            'Vigilante'  : (241, 213, 114),
            'Rogue'      : (180, 180, 180),
            'Resistance' : ( 30, 240, 255),
            'Loyalist'   : (255, 226,  56),
        }[self.GetState('Alignment')]
        self.nameBox.SetBackgroundColour(bgcolor)
        self.NameDisplay.SetBackgroundColour(bgcolor)
        # Have to do this dance to make the colors refresh on Windows.  Ugh.
        self.nameBox.Show(False)
        self.nameBox.Show(True)

        if evt: evt.Skip()

    def OnPickArchetype(self, evt = None):
        arch = self.GetState('Archetype')

        if not arch:
            wx.LogError("Got into OnPickArchetype with arch not set, bailing.  This is a bug.")
            return

        self.Ctrls['Primary'].Clear()
        self.Ctrls['Secondary'].Clear()
        self.Ctrls['Epic'].Clear()

        Primaries   = GameData.Archetypes[arch]['Primary']
        Secondaries = GameData.Archetypes[arch]['Secondary']
        Epix        = GameData.Archetypes[arch]['Epic']

        self.Ctrls['Epic'].Append('') # allow us to deselect epic pool

        for p in Primaries   : self.Ctrls['Primary'].Append(p)
        for s in Secondaries : self.Ctrls['Secondary'].Append(s)
        for e in Epix        : self.Ctrls['Epic'].Append(e)

        self.Ctrls['Primary'].SetSelection(0)
        self.Ctrls['Secondary'].SetSelection(0)
        self.Ctrls['Epic'].SetSelection(0)

        self.Ctrls['Epic'].Enable(arch != "Peacebringer" and arch != "Warshade")

        if getattr(self.Profile, 'Mastermind', None):
            self.Profile.Mastermind.SynchronizeUI()
        if getattr(self.Profile, 'MovementPowers', None):
            self.Profile.MovementPowers.SynchronizeUI()

        self.ArchetypeIcon.SetBitmap(GetIcon("Archetypes/" + arch))

        if evt: evt.Skip()

    def OnPickOrigin(self, evt = None):
        self.OriginIcon.SetBitmap(GetIcon('Origins/' + self.GetState('Origin')))
        if evt: evt.Skip()

    def OnPickPoolPower(self, evt):
        self.Profile.MovementPowers.SynchronizeUI()
        evt.Skip()

    def OnPickPrimaryPowerSet(self, evt):
        self.Profile.Mastermind.SynchronizeUI()
        evt.Skip()

    def OnPickSecondaryPowerSet(self, evt):
        evt.Skip()

    def OnPickEpicPowerSet(self, evt):
        evt.Skip()

    # def OnColorEnable(self, evt = None):
    #     colorsenabled = self.GetState('ChatColorEnable')
    #     self.EnableControls(colorsenabled, ['ChatBorder', 'ChatBackground', 'ChatForeground'])
    #     if evt: evt.Skip()

    def OnTypeEnable(self, evt = None):
        typeenabled = self.GetState('TypingNotifierEnable')
        self.EnableControls(typeenabled, ['TypingNotifier'])
        if typeenabled:
            self.Ctrls['StartChat'].CtlLabel.SetLabel('Start Chat (with Notifier):')
        else:
            self.Ctrls['StartChat'].CtlLabel.SetLabel('Start Chat:')
        self.Layout()
        if evt: evt.Skip()

    UI.Labels.update({
        'Pool1'           : "Power Pool 1",
        'Pool2'           : "Power Pool 2",
        'Pool3'           : "Power Pool 3",
        'Pool4'           : "Power Pool 4",

        'StartChat'            : 'Start Chat',
        'SlashChat'            : 'Start Chat (with "/")',
        'StartEmote'           : 'Begin emote (types "/em")',
        'AutoReply'            : 'AutoReply to incoming /tell',
        'TellTarget'           : 'Send /tell to current target',
        'QuickChat'            : 'Pop up QuickChat menu',

        'TypingNotifierEnable' : 'Enable Typing Notifier',
        'TypingNotifier'       : 'Typing Notifier',
    })
