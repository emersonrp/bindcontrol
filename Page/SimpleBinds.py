import wx

from wx.richtext import RichTextCtrl as RTC
from CustomBind import CustomBind
from Page import Page

class SimpleBinds(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Binds = ()
        self.TabTitle = "Simple Binds"

    def FillTab(self):
        profile = self.Profile

        self.MainSizer = wx.BoxSizer(wx.VERTICAL) # overall sizer
        self.PaneSizer = wx.BoxSizer(wx.VERTICAL) # sizer for collapsable panes
        buttonSizer    = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item button

        # Stick a button in the bottom sizer
        newBindButton = wx.Button(self, -1, "New Simple Item")
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

        bind = SimpleBind(self, bindinit)

        # TODO - if bind is already in there, just scroll to it and pop it open
        bindCP = wx.CollapsiblePane(self, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, bindCP)


        bind.PopulateCP(bindCP)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount() - 1, bindCP, 0, wx.ALL|wx.EXPAND, 10)
        self.Layout()


        #return bindCP

    def OnPaneChanged(self, event):
        self.Layout()


        #sub addSBind {
        #    my (sbinds,n,profile) #  this returns an IUP vbox/hbox to be inserted into the SBind Page box
        #    my sbind = sbinds[n]
        #    my sbtitle = cbTextBox("Bind Name",sbind.title,cbTextBoxCB(profile,sbind,"title"),200,nil,100)
        #    cbToolTip("Choose the Key Combo for this bind")
        #    # my bindkey = cbBindBox("Bind Key",sbind,"Key",function() return "SB: "..sbind.Command },profile,200)
        #    my bindkey = cbBindBox("Bind Key",sbind,"Key",cbMakeDescLink("Simple Bind ",sbind,"title"),profile,200)
        #    cbToolTip("Enter the Commands to be run when the Key Combo is pressed")
        #    # my bindcmd = cbTextBox("Bind Command",sbind.Command,cbTextBoxCB(profile,sbind,"Command"),200,nil,100)
        #    my bindcmd = cbPowerBindBtn("Bind Command",sbind,"Command",nil,300,nil,profile)
        #    cbToolTip("Click this to Delete this Bind, it will ask for confirmation before deleting")
        #    my delbtn = cbButton("Delete this Bind",function()
        #        if (iup.Alarm("Confirm Deletion","Are you sure you want to delete this bind?","Yes","No") == 1) {
        #            table.remove(sbinds,n)
        #            sbinds.curbind = sbinds.curbind - 1
        #            if (sbinds.curbind == 0) { sbinds.curbind = 1 }
        #            sbinds.dlg:hide()
        #            # sbinds.dlg:destroy()
        #            sbinds.dlg = nil
        #            createDialog(sbinds,profile)
        #            cbShowDialog(sbinds.dlg,218,10,profile,sbinds.dlg_close_cb)
        #            profile.modified = true 
        #        } },150)
        #    my exportbtn = cbButton("Export...",function() cbExportPageSettings(profile,n,sbinds,"SimpleBind",true) },150)
        #    return iup.frame{iup.vbox{sbtitle,bindkey,bindcmd,iup.hbox{delbtn,exportbtn}},cx = 0, cy = 65 * (n-1)}
        #}

    #sub newSBind { return { Command => newPowerBind() } }

        #my $box = []
        #for my $i (1..length @$sbinds) {
            #push @$box, addSBind($sbinds, $i, $profile)
        #}
        #$sbinds->{'curbind'} ||= 1
    #    cbToolTip("Click this to add a new bind")
    #    my newbindbtn = cbButton("New Simple Bind",
    #        function()
    #            table.insert(sbinds,newSBind())
    #            sbinds.curbind = table.getn(sbinds)
    #            sbinds.dlg:hide()
    #            # sbinds.dlg:destroy()
    #            sbinds.dlg = nil
    #            createDialog(sbinds,profile)
    #            cbShowDialog(sbinds.dlg,218,10,profile,sbinds.dlg_close_cb)
    #            profile.modified = true 
    #        },100)
    #    my importbtn = cbButton("Import Simple Bind",function()
    #        #  get the simple binds contained in a selected Page.
    #        my importtable = cbImportPageSettings(profile,nil,nil,"SimpleBind",true)
    #        if (not importtable) { return }
    #        for i,v in ipairs(importtable) do
    #            table.insert(sbinds,v)
    #        }
    #        # my newsbind_n = table.getn(sbinds)
    #        sbinds.curbind = table.getn(sbinds)
    #        sbinds.dlg:hide()
    #        sbinds.dlg = nil
    #        #  Resolve Key COnflicts.
    #        cbResolveKeyConflicts(profile,true)
    #        createDialog(sbinds,profile)
    #        cbShowDialog(sbinds.dlg,218,10,profile,sbinds.dlg_close_cb)
    #        profile.modified = true
    #    },100)
    #    my sbEnablePrev = "NO"
    #    my sbEnableNext = "NO"
    #    if (sbinds.curbind > 1) { sbEnablePrev = "YES" }
    #    cbToolTip("Click this to go to the previous bind")
    #    sbinds.prevbind = cbButton("<<",function(self)
    #            sbinds.curbind = sbinds.curbind - 1
    #            if (sbinds.curbind < 1) { sbinds.curbind = 1 }
    #            sbinds.zbox.value = box[sbinds.curbind]
    #            sbinds.poslabel.title = sbinds.curbind.."/"..table.getn(sbinds)
    #            my sbEnablePrev = "NO"
    #            if (sbinds.curbind > 1) { sbEnablePrev = "YES" }
    #            sbinds.prevbind.active=sbEnablePrev
    #            my sbEnableNext = "NO"
    #            if (sbinds.curbind < table.getn(sbinds)) { sbEnableNext = "YES" }
    #            sbinds.nextbind.active=sbEnableNext
    #        },25,nil,{active=sbEnablePrev})
    #    if (sbinds.curbind < table.getn(sbinds)) { sbEnableNext = "YES" }
    #    cbToolTip("Click this to go to the previous bind")
    #    sbinds.nextbind = cbButton(">>",function(self)
    #            sbinds.curbind = sbinds.curbind + 1
    #            if (sbinds.curbind > table.getn(sbinds)) { sbinds.curbind = table.getn(sbinds) }
    #            sbinds.zbox.value = box[sbinds.curbind]
    #            sbinds.poslabel.title = sbinds.curbind.."/"..table.getn(sbinds)
    #            my sbEnablePrev = "NO"
    #            if (sbinds.curbind > 1) { sbEnablePrev = "YES" }
    #            sbinds.prevbind.active=sbEnablePrev
    #            my sbEnableNext = "NO"
    #            if (sbinds.curbind < table.getn(sbinds)) { sbEnableNext = "YES" }
    #            sbinds.nextbind.active=sbEnableNext
    #        },25,nil,{active=sbEnableNext})
    #    sbinds.poslabel = iup.label{title = sbinds.curbind.."/"..table.getn(sbinds);rastersize="50x";alignment="ACENTER"}
    #    box.value = box[sbinds.curbind]
    #    sbinds.zbox = iup.zbox(box)
    #    sbinds.dlg = iup.dialog{iup.vbox{sbinds.zbox,iup.hbox{sbinds.prevbind;newbindbtn;importbtn;sbinds.poslabel;sbinds.nextbind;alignment="ACENTER"};alignment="ACENTER"};title = "General : Simple Binds",maxbox="NO",resize="NO",mdichild="YES",mdiclient=mdiClient}
    #    sbinds.dlg_close_cb = function(self) sbinds.dlg = nil }
    #}

    #sub bindsettings {
        #my ($profile) = @_
        #my $sbinds = $profile->{'sbinds'}
        #unless ($sbinds) {
            #$profile->{'sbinds'} = $sbinds = {}
        #}
        #if ($sbinds->{'dlg'}) {
    #        sbinds.dlg:show()
        #} else {
    #        createDialog(sbinds,profile)
    #        cbShowDialog(sbinds.dlg,218,10,profile,sbinds.dlg_close_cb)
        #}
    #}

    def PopulateBindFiles(self):
        profile   = self.Profile
        ResetFile = profile.ResetFile

        for b in self.State['binds'].items():
            ResetFile.SetBind(b['key'], Utility.cpBindToString(b['payload']))

    def findconflicts(self):
        for b in self.State['binds'].items():
            Utility.CheckConflict(
                b['key'], "Key", "Simple Bind " + (b['title'] or "Unknown")
            )

    def bindisused(self, profile):
        return bool(len(self.State('binds')))

### CustomBind subclasses for the indibidual bind types

class SimpleBind(CustomBind):
    def __init__(self, page, bind):
        CustomBind.__init__(self, page, bind)

    def PopulateCP(self, BindCP):

        BindCP.SetLabel("This is a test label")
        pane = BindCP.GetPane()

        # TODO:
        # payload  = RTC(pane, -1, "testing 1 2 3", style=wx.richtext.RE_MULTILINE)
        # payload.SetHint("/say Your bind text goes here!$$powexec Super Jump")

        BindSizer = wx.GridBagSizer(hgap=5, vgap=5)

        BindSizer.Add(wx.StaticText(pane, -1, "Bind Name:"),     (0,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.TextCtrl  (pane, -1, ""),               (0,1), flag=wx.EXPAND)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Key:"),      (0,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.Button    (pane, -1, "UNBOUND"),        (0,3), flag=wx.EXPAND)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Contents:"), (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.TextCtrl(pane, -1),                     (1,1), span=(1,3), flag=wx.ALL|wx.EXPAND)

        BindSizer.AddGrowableCol(1)
        BindSizer.AddGrowableCol(3)

        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 1, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)
