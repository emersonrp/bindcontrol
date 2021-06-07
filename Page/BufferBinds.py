import wx
import Utility
import UI

from wx.richtext import RichTextCtrl as RTC
from CustomBind import CustomBind
from Page import Page
from UI.ControlGroup import ControlGroup

class BufferBinds(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Binds = {}
        self.TabTitle = "Buffer Binds"
        self.State = {
            'BuffPetsByName' : True,
            'BuffsAffectTeam': True,
            'BuffsAffectPets': True,
        }

        for i in (1,2,3,4,5,6,7,8):
            self.State[f"Team{i}BuffKey"] = "UNBOUND"

        for i in (1,2,3,4,5,6):
            self.State[f"Pet{i}BuffKey"] = "UNBOUND"

    def FillTab(self):
        profile = self.Profile

        self.MainSizer = wx.BoxSizer(wx.VERTICAL) # overall sizer
        self.PaneSizer = wx.BoxSizer(wx.VERTICAL) # sizer for collapsable panes
        buttonSizer    = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item button

        # Stick a button in the bottom sizer
        newBindButton = wx.Button(self, -1, "New Buffer Bind")
        newBindButton.Bind(wx.EVT_BUTTON, self.AddBindToPage)
        buttonSizer.Add(newBindButton, wx.ALIGN_CENTER)

        # Put blank space into PaneSizer so it expands
        self.PaneSizer.AddStretchSpacer()

        # add the two sub-sizers, top one expandable
        self.MainSizer.Add( self.PaneSizer, 1, wx.EXPAND|wx.ALL)
        self.MainSizer.Add( buttonSizer, 0, wx.EXPAND|wx.ALL)

        # sizer around the whole thing to add padding
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(self.MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        # Add any binds that came from a savefile
        for bind in self.Binds:
            bindCP = self.AddBindToPage(bind)

        self.SetSizerAndFit(paddingSizer)
        self.Layout()

    def AddBindToPage(self, _, bindinit = {}):

        bind = BufferBind(self, bindinit)

        # TODO - if bind is already in there, just scroll to it and pop it open
        bindCP = wx.CollapsiblePane(self, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, bindCP)


        bind.PopulateCP(bindCP)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount() - 1, bindCP, 0, wx.ALL|wx.EXPAND, 10)
        self.Layout()


        #return bindCP

    def OnPaneChanged(self, event):
        self.Layout()








    def addBufferBindSetToDialog(self, bind):

        ###
        # TODO - all of this is still TCL from citybinder
        # TODO - this should be just the add-to-gui logic
        #        where the bind might come from "new" or from a loaded profile
        ###

        pass

    #    bbind = $bufferbinds[$n]
    #    bbtitle = cbTextBox("Buffer Bind Name",bbind['title'],cbTextBoxCB($profile,$bbind,"title"),300,undef,100)
    #    # selchattext = cbToggleText("Select Chat",bbind['selchatenabled'],bbind['selchat'],
    #        # cbCheckBoxCB($profile,$bbind,"selchatenabled"),cbTextBoxCB($profile,$bbind,"selchat"),100,undef,300)
    #    selchattext = cbPowerBindBtn("Select Chat",$bbind,"selchat",chatnogloballimit,300,undef,$profile)
    #    # buffpower1 = cbTextBox("Buff Power",bbind['power1'],cbTextBoxCB($profile,$bbind,"power1"))
    #    buffpower1 = cbPowerList("First Buff Power",$profile.{'powerset'},$bbind,"power1",$profile,200)
    #    chat1text = cbPowerBindBtn("First Chat Command",$bbind,"chat1",chatnogloballimit,300,undef,$profile)
    #    chat3text = cbPowerBindBtn("Third Chat Command",$bbind,"chat3",chatnogloballimit,300,undef,$profile)
    #    if (not bbind['power3enabled']) { chat3text.active = "NO" }
    #    buffpower3 = cbTogglePower("Third Buff Power",$profile.{'powerset'},bbind['power3enabled'],$bbind,"power3",
    #        sub { my(_,v) $profile.{'modified'} = true 
    #            if (v == 1) {
    #                bbind['power3enabled'] = true
    #                chat3text.active = "YES"
    #            } else {
    #                bbind['power3enabled'] = undef
    #                chat3text.active = "NO"
    #            }
    #        },$profile,undef,undef,200)
    #    if (not bbind['power2enabled']) { buffpower3.active = "NO" }
    #    chat2text = cbPowerBindBtn("Second Chat Command",$bbind,"chat2",chatnogloballimit,300,undef,$profile)
    #    if (not bbind['power2enabled']) { chat2text.active = "NO" }
    #    buffpower2 = cbTogglePower("Second Buff Power",$profile.{'powerset'},bbind['power2enabled'],$bbind,"power2",
    #        sub { my(_,v) $profile.{'modified'} = true 
    #            if (v == 1) {
    #                bbind['power2enabled'] = true
    #                chat2text.active = "YES"
    #                buffpower3.active = "YES"
    #                if (bbind['power3enabled']) {
    #                    chat3text.active = "YES"
    #                }
    #            } else {
    #                bbind['power2enabled'] = undef
    #                chat2text.active = "NO"
    #                buffpower3.active = "NO"
    #                chat3text.active = "NO"
    #            }
    #        },$profile,undef,undef,200)
    #    team1key = cbBindBox("Team 1 Key",$bbind,"team1",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 1 Key"),$profile)
    #    team2key = cbBindBox("Team 2 Key",$bbind,"team2",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 2 Key"),$profile)
    #    team3key = cbBindBox("Team 3 Key",$bbind,"team3",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 3 Key"),$profile)
    #    team4key = cbBindBox("Team 4 Key",$bbind,"team4",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 4 Key"),$profile)
    #    team5key = cbBindBox("Team 5 Key",$bbind,"team5",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 5 Key"),$profile)
    #    team6key = cbBindBox("Team 6 Key",$bbind,"team6",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 6 Key"),$profile)
    #    team7key = cbBindBox("Team 7 Key",$bbind,"team7",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 7 Key"),$profile)
    #    team8key = cbBindBox("Team 8 Key",$bbind,"team8",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 8 Key"),$profile)
    #    usepetnames = cbCheckBox("Use Pet Names to Select?",bbind['usepetnames'],cbCheckBoxCB($profile,$bbind,"usepetnames"))
    #    pet1key = cbBindBox("Pet 1 Key",$bbind,"pet1",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 1 Key"),$profile)
    #    pet2key = cbBindBox("Pet 2 Key",$bbind,"pet2",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 2 Key"),$profile)
    #    pet3key = cbBindBox("Pet 3 Key",$bbind,"pet3",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 3 Key"),$profile)
    #    pet4key = cbBindBox("Pet 4 Key",$bbind,"pet4",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 4 Key"),$profile)
    #    pet5key = cbBindBox("Pet 5 Key",$bbind,"pet5",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 5 Key"),$profile)
    #    pet6key = cbBindBox("Pet 6 Key",$bbind,"pet6",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 6 Key"),$profile)
    #    #  we use a custom listbox callback to enable/disable bufferbind UI elements based on the selection of this list.
    #    target = cbListBox("Buffs affect...",{"Teammates","Pets","Both"},3,bbind['target'],
    #        sub { my(_,str,i,v) $profile.{'modified'} = true 
    #            if (v == 1) {
    #                bbind['target'] = i
    #                #  activate bind boxes based on the value of i.
    #                if (i == 1) {
    #                    team1key.active="YES"
    #                    team2key.active="YES"
    #                    team3key.active="YES"
    #                    team4key.active="YES"
    #                    team5key.active="YES"
    #                    team6key.active="YES"
    #                    team7key.active="YES"
    #                    team8key.active="YES"
    #                    pet1key.active="NO"
    #                    pet2key.active="NO"
    #                    pet3key.active="NO"
    #                    pet4key.active="NO"
    #                    pet5key.active="NO"
    #                    pet6key.active="NO"
    #                } elsif (i == 2) {
    #                    team1key.active="NO"
    #                    team2key.active="NO"
    #                    team3key.active="NO"
    #                    team4key.active="NO"
    #                    team5key.active="NO"
    #                    team6key.active="NO"
    #                    team7key.active="NO"
    #                    team8key.active="NO"
    #                    pet1key.active="YES"
    #                    pet2key.active="YES"
    #                    pet3key.active="YES"
    #                    pet4key.active="YES"
    #                    pet5key.active="YES"
    #                    pet6key.active="YES"
    #                } else {
    #                    team1key.active="YES"
    #                    team2key.active="YES"
    #                    team3key.active="YES"
    #                    team4key.active="YES"
    #                    team5key.active="YES"
    #                    team6key.active="YES"
    #                    team7key.active="YES"
    #                    team8key.active="YES"
    #                    pet1key.active="YES"
    #                    pet2key.active="YES"
    #                    pet3key.active="YES"
    #                    pet4key.active="YES"
    #                    pet5key.active="YES"
    #                    pet6key.active="YES"
    #                }
    #            }
    #        })
    #    if (bbind['target'] == 1) {
    #        pet1key.active="NO"
    #        pet2key.active="NO"
    #        pet3key.active="NO"
    #        pet4key.active="NO"
    #        pet5key.active="NO"
    #        pet6key.active="NO"
    #    } elsif (bbind['target'] == 2) {
    #        team1key.active="NO"
    #        team2key.active="NO"
    #        team3key.active="NO"
    #        team4key.active="NO"
    #        team5key.active="NO"
    #        team6key.active="NO"
    #        team7key.active="NO"
    #        team8key.active="NO"
    #    }
    #
    #    delbtn = cbButton("Delete this Bind",sub {
    #        if (iup.Alarm("Confirm Deletion","Are you sure you want to delete this bind?","Yes","No") == 1) {
    #            table.remove($bufferbinds,n)
    #            $bufferbinds.{'curset'} = $bufferbinds.{'curset'} - 1
    #            if ($bufferbinds.{'curset'} == 0) { $bufferbinds.{'curset'} = 1 }
    #            cbCleanDlgs($profile,$bufferbinds.{'dlg'})
    #            $bufferbinds.{'dlg'}:hide()
    #            # $bufferbinds.{'dlg'}:destroy()
    #            $bufferbinds.{'dlg'} = undef
    #            module.createDialog($bufferbinds,$profile)
    #            cbShowDialog($bufferbinds.{'dlg'},218,10,$profile,$bufferbinds.{'dlg_close_cb'})
    #            $profile.{'modified'} = true 
    #        }
    #    })
    #    exportbtn = cbButton("Export...",sub { cbExportPageSettings($profile,n,$bufferbinds,"BuffBind") })
    #
    #    return iup.vbox{bbtitle,selchattext,buffpower1,chat1text,buffpower2,chat2text,buffpower3,chat3text,
    #        iup.hbox{iup.vbox{team1key,team2key,team3key,team4key,team5key,team6key,team7key,team8key},
    #            iup.vbox{target,iup.fill{},usepetnames,pet1key,pet2key,pet3key,pet4key,pet5key,pet6key,iup.fill{}}},
    #        iup.hbox{delbtn,exportbtn}
    #    }
    #    box = {}
    #    for i = 1,table.getn($bufferbinds) do
    #        table.insert(box,addBBind($bufferbinds,i,$profile))
    #    }
    #    $bufferbinds.{'curset'} = $bufferbinds.{'curset'} or 1
    #    cbToolTip("Click this to add a new bind")
    #    newbindbtn = cbButton("New Buff Bind",
    #        sub {
    #            table.insert($bufferbinds,newBBind())
    #            $bufferbinds.{'curbind'} = table.getn($bufferbinds)
    #            $bufferbinds.{'dlg'}:hide()
    #            # $bufferbinds.{'dlg'}:destroy()
    #            $bufferbinds.{'dlg'} = undef
    #            module.createDialog($bufferbinds,$profile)
    #            cbShowDialog($bufferbinds.{'dlg'},218,10,$profile,$bufferbinds.{'dlg_close_cb'})
    #            $profile.{'modified'} = true
    #        },100)
    #    importbtn = cbButton("Import Buff Bind",sub {
    #        new$bbind = newBBind() #  we will be filling this new BBind up.
    #        table.insert($bufferbinds,new$bbind)
    #        new$bbind_n = table.getn($bufferbinds)
    #        if (cbImportPageSettings($profile,new$bbind_n,$bufferbinds,"BuffBind")) {
    #            $bufferbinds.{'curbind'} = table.getn($bufferbinds)
    #            $bufferbinds.{'dlg'}:hide()
    #            $bufferbinds.{'dlg'} = undef
    #            #  Resolve Key COnflicts.
    #            cbResolveKeyConflicts($profile,true)
    #            module.createDialog($bufferbinds,$profile)
    #            cbShowDialog($bufferbinds.{'dlg'},218,10,$profile,$bufferbinds.{'dlg_close_cb'})
    #            $profile.{'modified'} = true
    #        } else {
    #            #  user cancelled, remove the new table from $bufferbinds.
    #            table.remove($bufferbinds)
    #        }
    #    },100)
    #    bbEnablePrev = "NO"
    #    bbEnableNext = "NO"
    #    if ($bufferbinds.{'curset'} > 1) { bbEnablePrev = "YES" }
    #    cbToolTip("Click this to go to the previous bind")
    #    $bufferbinds.{'prevbind'} = cbButton("<<",sub { my(self)
    #            $bufferbinds.{'curset'} = $bufferbinds.{'curset'} - 1
    #            if ($bufferbinds.{'curset'} < 1) { $bufferbinds.{'curset'} = 1 }
    #            $bufferbinds.{'zbox'}.value = box[$bufferbinds.{'curset'}]
    #            $bufferbinds.{'poslabel'}.title = $bufferbinds.{'curset'}.."/"..table.getn($bufferbinds)
    #            bbEnablePrev = "NO"
    #            if ($bufferbinds.{'curset'} > 1) { bbEnablePrev = "YES" }
    #            $bufferbinds.{'prevbind'}.active=bbEnablePrev
    #            bbEnableNext = "NO"
    #            if ($bufferbinds.{'curset'} < table.getn($bufferbinds)) { bbEnableNext = "YES" }
    #            $bufferbinds.{'nextbind'}.active=bbEnableNext
    #        },25,undef,{active=bbEnablePrev})
    #    if ($bufferbinds.{'curset'} < table.getn($bufferbinds)) { bbEnableNext = "YES" }
    #    cbToolTip("Click this to go to the previous bind")
    #    $bufferbinds.{'nextbind'} = cbButton(">>",sub { my(self)
    #            $bufferbinds.{'curset'} = $bufferbinds.{'curset'} + 1
    #            if ($bufferbinds.{'curset'} > table.getn($bufferbinds)) { $bufferbinds.{'curset'} = table.getn($bufferbinds) }
    #            $bufferbinds.{'zbox'}.value = box[$bufferbinds.{'curset'}]
    #            $bufferbinds.{'poslabel'}.title = $bufferbinds.{'curset'}.."/"..table.getn($bufferbinds)
    #            bbEnablePrev = "NO"
    #            if ($bufferbinds.{'curset'} > 1) { bbEnablePrev = "YES" }
    #            $bufferbinds.{'prevbind'}.active=bbEnablePrev
    #            bbEnableNext = "NO"
    #            if ($bufferbinds.{'curset'} < table.getn($bufferbinds)) { bbEnableNext = "YES" }
    #            $bufferbinds.{'nextbind'}.active=bbEnableNext
    #        },25,undef,{active=bbEnableNext})
    #    $bufferbinds.{'poslabel'} = iup.label{title = $bufferbinds.{'curset'}.."/"..table.getn($bufferbinds);rastersize="50x";alignment="ACENTER"}
    #    box.value = box[$bufferbinds.{'curset'}]
    #    $bufferbinds.{'zbox'} = iup.zbox(box)
    #    $bufferbinds.{'dlg'} = iup.dialog{iup.vbox{$bufferbinds.{'zbox'},iup.hbox{$bufferbinds.{'prevbind'};newbindbtn;importbtn;$bufferbinds.{'poslabel'};$bufferbinds.{'nextbind'};alignment="ACENTER"};alignment="ACENTER"};title = "Gameplay : Buffer Binds",maxbox="NO",resize="NO",mdichild="YES",mdiclient=mdiClient}
    #    $bufferbinds.{'dlg_close_cb'} = sub { my(self) $bufferbinds.{'dlg'} = undef }

    def PopulateBindFiles(self):
        profile = self.Profile
        ResetFile = profile.ResetFile

        buffer = self.State['buffer']

        for key in buffer:
            bbind = buffer['key']

            if bbind.get('selchatenabled', None):
                chat1 = cbPBindToString(bbind['chat1'])
                chat2 = cbPBindToString(bbind['chat2'])
                chat3 = cbPBindToString(bbind['chat3'])

            npow = 1
            if bbind.get('power2enabled', None):
                npow = 2
                if (bbind.get('power3enabled')): npow = 3

            if ((bbind['target'] == 1) or (bbind['target'] == 3)):
                for j in range(1,9):
                    teamid = "team"+j
                    filebase = f"{profile['base']}\\buff{i}\\bufft{j}"
                    afile = profile.GetBindFile(f"{filebase}a.txt")
                    bfile = profile.GetBindFile(f"{filebase}b.txt")
                    afile.SetBind(    teamid, f'+down$$teamselect {j}$${selchat}bindloadfile {filebase}b.txt')
                    ResetFile.SetBind(teamid, f'+down$$teamselect {j}$${selchat}bindloadfile {filebase}b.txt')
                    if (npow == 1):
                        bfile.SetBind(teamid,f'-down$${chat1}powexecname {bbind["power1"]}$$bindloadfile {filebase}a.txt')
                    else:
                        bfile.SetBind(teamid,f'-down$${chat1}powexecname {bbind["power1"]}$$bindloadfile {filebase}c.txt')
                        cfile = profile.GetBindFile(f"{filebase}c.txt")
                        if (npow == 2):
                            cfile.SetBind(teamid, f'{chat2}powexecname {bbind["power2"]}$$bindloadfile {filebase}a.txt')
                        else:
                            dfile = profile.GetBindFile(f"{filebase}d.txt")
                            cfile.SetBind(teamid, f'+down$${chat2}powexecname {bbind["power2"]}$$bindloadfile {filebase}d.txt')
                            dfile.SetBind(teamid, f'-down$${chat3}powexecname {bbind["power3"]}$$bindloadfile {filebase}a.txt')

            if ((bbind['target'] == 2) or (bbind['target'] == 3)):
                for j in range(1.7):
                    petid = "pet" + j
                    filebase = f"{profile['base']}\\buff{i}\\buffp{j}"
                    if (bbind['usepetnames']):
                        ResetFile.SetBind(petid, f'+down$$petselectname {profile["petaction"]}pet{j}name$${selchat}bindloadfile {filebase}b.txt')
                    else:
                        ResetFile.SetBind(petid, f'+down$$petselect {j-1}$${selchat}bindloadfile {filebase}b.txt')

                    afile = profile.GetBindFile(f"{filebase}a.txt")
                    bfile = profile.GetBindFile(f"{filebase}b.txt")
                    if (bbind['usepetnames']):
                        afile.SetBind(petid, f'+down$$petselectname {profile["petaction"]}pet{j}name$${selchat}bindloadfile {filebase}b.txt')
                    else:
                        afile.SetBind(petid, f'+down$$petselect {j-1}$${selchat}bindloadfile {filebase}b.txt')

                    if (npow == 1):
                        bfile.SetBind(petid, f'-down$${chat1}powexecname {bbind["power1"]}$$bindloadfile {filebase}a.txt')
                    else:
                        bfile.SetBind(petid, f'-down$${chat1}powexecname {bbind["power1"]}$$bindloadfile {filebase}c.txt')
                        cfile = profile.GetBindFile(f"{filebase}c.txt")
                        if (npow == 2):
                            cfile.SetBind(petid, f"{chat2}powexecname {bbind['power2']}$$bindloadfile {filebase}a.txt")
                        else:
                            dfile = profile.GetBindFile(f"{filebase}d.txt")
                            cfile.SetBind(petid, f'+down$${chat2}powexecname {bbind["power2"]}$$bindloadfile {filebase}d.txt')
                            dfile.SetBind(petid, f'-down$${chat3}powexecname {bbind["power3"]}$$bindloadfile {filebase}a.txt')

    def findconflicts(self, profile):
        for bbind in self.State['bufferbinds']:
            title = bbind.get('title', "unknown")
            if ((bbind['target'] == 1) or (bbind['target'] == 3)):
                for j in range(1,9):
                    Utility.CheckConflict(bbind,"team"+j, f"Buff bind {title}: Team {j} Key")

            if ((bbind['target'] == 2) or (bbind['target'] == 3)):
                for j in range(1,7):
                    Utility.CheckConflict(bbind,"pet"+j, f"Buff bind {title}: Pet {j} Key")

    def bindisused(self, profile):
        return bool(len(self.buffer.keys()))

    for i in (1,2,3,4,5,6,7,8):
        UI.Labels[f'Team{i}BuffKey'] = f"Team {i} Key"

    for i in (1,2,3,4,5,6):
        UI.Labels[f'Pet{i}BuffKey'] = f"Pet {i} Key"

    UI.Labels.update( {
        'BuffPetsByName' : "Buff Pets using Pet Names",
        'BuffsAffectTeam' : "Buffs Affect Team Members",
        'BuffsAffectPets' : "Buffs Affect Pets",
    })

### CustomBind subclasses for the indibidual bind types

class BufferBind(CustomBind):
    def __init__(self, page, bind):
        CustomBind.__init__(self, page, bind)
        self.Page = page

    def PopulateCP(self, BindCP):

        BindCP.SetLabel("This is a test label")
        pane = BindCP.GetPane()
        # TODO:
        # payload  = RTC(pane, -1, "testing 1 2 3", style=wx.richtext.RE_MULTILINE)
        # payload.SetHint("/say Your bind text goes here!$$powexec Super Jump")

        # bind text controls
        BindSizer = wx.GridBagSizer(hgap=5, vgap=5)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Name:"),     (0,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.TextCtrl  (pane, -1, ""),               (0,1), span=(1,4), flag=wx.EXPAND)

        BindSizer.Add(wx.StaticText(pane, -1, "First Buff Power"), (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(self.BuffPowerPicker(pane),                  (1,1), flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra"),            (1,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.TextCtrl  (pane, -1, ""),                 (1,3), flag=wx.EXPAND)
        BindSizer.Add(wx.Button(pane, -1, "..."),                  (1,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        BindSizer.Add(wx.StaticText(pane, -1, "Second Buff Power"),(2,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(self.BuffPowerPicker(pane),                  (2,1), flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra"),            (2,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.TextCtrl  (pane, -1, ""),                 (2,3), flag=wx.EXPAND)
        BindSizer.Add(wx.Button(pane, -1, "..."),                  (2,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        BindSizer.Add(wx.StaticText(pane, -1, "Third Buff Power"), (3,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(self.BuffPowerPicker(pane),                  (3,1), flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra"),            (3,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.TextCtrl  (pane, -1, ""),                 (3,3), flag=wx.EXPAND)
        BindSizer.Add(wx.Button(pane, -1, "..."),                  (3,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        BindSizer.Add(wx.StaticText(pane, -1, ""),                 (4,0))


        # key picker controls
        KeySizer = wx.BoxSizer(wx.HORIZONTAL)
        TeamCtrls = ControlGroup(pane, self.Page, "Buff Team Keybinds")
        PetCtrls  = ControlGroup(pane, self.Page, "Buff Pet Keybinds")

        TeamCtrls.AddLabeledControl(ctltype = 'checkbox', value = "BuffsAffectTeam")
        for i in (1,2,3,4,5,6,7,8):
            TeamCtrls.AddLabeledControl(ctltype = "keybutton", value = f"Team{i}BuffKey", contents = "UNBOUND")


        PetCtrls.AddLabeledControl(ctltype = 'checkbox', value = "BuffsAffectPets")
        PetCtrls.AddLabeledControl(ctltype = "checkbox", value = "BuffPetsByName")
        for i in (1,2,3,4,5,6):
            PetCtrls.AddLabeledControl(ctltype = "keybutton", value = f"Pet{i}BuffKey", contents = "UNBOUND")

        KeySizer.Add(TeamCtrls, 0, flag = wx.LEFT|wx.RIGHT, border = 5)
        KeySizer.Add(PetCtrls,  0, flag = wx.LEFT|wx.RIGHT, border = 5)

        BindSizer.AddGrowableCol(1)
        BindSizer.AddGrowableCol(3)
        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 10)
        border.Add(KeySizer,  0, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)


    def BuffPowerPicker(self, pane):
        picker = wx.Choice(pane, -1)
        return picker
