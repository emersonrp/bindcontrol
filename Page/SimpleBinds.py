import wx
from CustomBind import CustomBind
from Page import Page
from UI.ControlGroup import ControlGroup

class SimpleBinds(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Binds = ()
        self.TabTitle = "Simple Binds"

    def FillTab(self):
        profile = self.Profile

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)

        newBindButton = wx.Button(self, -1, "New Simple Item")
        newBindButton.Bind(wx.EVT_BUTTON, self.AddBindToPage)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(newBindButton, wx.ALIGN_CENTER)

        self.MainSizer.Add( buttonSizer, 0, wx.EXPAND|wx.ALL)


        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(self.MainSizer, flag = wx.ALL|wx.EXPAND, border = 16)

        # Create collapsable tree for list of binds, each with their appropriate UI.
        for bind in self.Binds:
            bindCP = self.AddBindToPage(bind)

        self.SetSizerAndFit(paddingSizer)
        self.Layout()

    def AddBindToPage(self, _, bindinit = {}):

        ###
        # TODO - all of this is still TCL from citybinder
        # TODO - this should be just the add-to-gui logic
        #        where the bind might come from "new" or from a loaded profile
        ###

        bind = SimpleBind(bindinit)

        # TODO - if bind is already in there, just scroll to it and pop it open
        bindCP = wx.CollapsiblePane(self, label = "Fake Item For Debug",
                                        style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, bindCP)

        self.MainSizer.Add(bindCP, 1, wx.ALL|wx.EXPAND, 10)

        bind.PopulateCP(bindCP.GetPane())

        return bindCP

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
    def __init__(self, bind):
        CustomBind.__init__(self, bind)

    def PopulateCP(self, pane):

        nameLbl = wx.StaticText(pane, -1, "Name:")
        name = wx.TextCtrl(pane, -1, "");

        addrLbl = wx.StaticText(pane, -1, "Address:")
        addr1 = wx.TextCtrl(pane, -1, "");
        addr2 = wx.TextCtrl(pane, -1, "");

        cstLbl = wx.StaticText(pane, -1, "City, State, Zip:")
        city  = wx.TextCtrl(pane, -1, "", size=(150,-1));
        state = wx.TextCtrl(pane, -1, "", size=(50,-1));
        zip   = wx.TextCtrl(pane, -1, "", size=(70,-1));

        addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addrSizer.AddGrowableCol(1)
        addrSizer.Add(nameLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(name, 0, wx.EXPAND)
        addrSizer.Add(addrLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(addr1, 0, wx.EXPAND)
        addrSizer.Add((5,5))
        addrSizer.Add(addr2, 0, wx.EXPAND)

        addrSizer.Add(cstLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        cstSizer = wx.BoxSizer(wx.HORIZONTAL)
        cstSizer.Add(city, 1)
        cstSizer.Add(state, 0, wx.LEFT|wx.RIGHT, 5)
        cstSizer.Add(zip)
        addrSizer.Add(cstSizer, 0, wx.EXPAND)

        # border sizer inside the pane
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 16)
        pane.SetSizer(border)

        pane.Layout()
