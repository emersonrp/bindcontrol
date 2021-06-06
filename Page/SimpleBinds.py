import wx
from Page import Page

class SimpleBinds(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.State = {
            'binds': ()
        }
        self.TabTitle = "Simple Binds"



    def FillTab(self):
        profile = self.Profile

        sizer = wx.BoxSizer(wx.VERTICAL)

        newBuffBindButton = wx.Button(self, -1, "New Simple Bind")
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(newBuffBindButton, wx.ALIGN_CENTER)

        sizer.Add( buttonSizer, 0, wx.EXPAND|wx.ALL)

        for bbs in self.State['binds']:
            self.addBindToDialog(bbs)


        self.SetSizerAndFit(sizer)

        self.Layout()

    def addSimpleBindToDialog(self, bind):

        ###
        # TODO - all of this is still TCL from citybinder
        # TODO - this should be just the add-to-gui logic
        #        where the bind might come from "new" or from a loaded profile
        ###

        pass

        #sub addSBind {
        #    my (sbinds,n,profile) #  this returns an IUP vbox/hbox to be inserted into the SBind Dialog box
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
        ResetFile = profile.Pages['General']['ResetFile']

        for b in self.State['binds'].items():
            ResetFile.SetBind(b['key'], Utility.cpBindToString(b['payload']))

    def findconflicts(self):
        for b in self.State['binds'].items():
            Utility.cbCheckConflict(
                b['key'], "Key", "Simple Bind " + (b['title'] or "Unknown")
            )

    def bindisused(self, profile):
        return bool(len(self.State('binds')))

class SimpleBind():
    def __init__(self, bind):
        self.Key = ''
        self.Title = ''
        self.Payload

        if bind.get('key',     None): self.Key     = bind['key']
        if bind.get('title',   None): self.Title   = bind['title']
        if bind.get('payload', None): self.Payload = bind['payload']
