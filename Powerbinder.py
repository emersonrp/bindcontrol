import PowerBindCmds

cmds = {}
cmdlist = []

def addCmd(label, new, form, make, match, c = cmds, clist = cmdlist):
    c[label] = {}
    c[label]['new'] = new
    c[label]['form'] = form
    c[label]['make'] = make
    c[label]['match'] = match
    clist.append(label)

def cbPBindToString(a, profile):
    if not a: return
    c = a['limit']['cmds'] or cmds

    string = ""
    prefix = ""
    for _,v in a.items():
        string = string + prefix + c[v.type].make(v, profile)
        prefix = "$$"
    return string

# Each bind command needs its own set of three functions, a form creation
# function, a new or creation function, and a makebind function.

# The form creation function takes an argument t, which is the table
# representing the bind command.  The form command must create a field,
# settings, on t, equal to the iup.frame containing all the UI allowing the CB
# user to change the settings for this bind command.  The form must then return
# t.

# The new/creation function for a bind command creates the table used in the
# form and make functions.  any default settings should be placed in t as in
# t.method or t.power, etc.  this function also MUST supply a t.type variable,
# with the name of the Bind Command.  and it MUST NOT use t.settings, as this
# is used in the form function.  Otherwise, all other names are fair game, and
# even numbers can be used, like t[1], t[2], etc.

# The make command simply creates the string that would be ordinarily typed
# inbetween $$'s in a bind command.  It can use any of the stuff set up in the
# new function, and anything set up in the UI functions from the form function.

# Finally, addCmd has to be called to add the command functions to the list of
# bind commands that CB knows about.

# A given PowerBind is essentially a table with integer index entries
# containing the commands to execute, in order, for the bind.  The powerbind
# table also has a container for IUp elements for dynamic changes

#creation functions for powerbind dialog goes here


def refreshCmds(bind,limit,profile,refreshcb):
        t = []
        # detach each command from the bind, then reattach.  this should be
        # done after reordering or deleting.

        for k,v in bind.items():
            # TODO this is ui stuff
            # if v.cmd:
                # iup.Detach(v.cmd)
                # iup.Destroy(v.cmd)
            t.append(v)

        bind = { 'order' : {} }
        for v in t:
            #  --cmds[v.type].form(v)
            formCommand(v,bind,limit,true,profile,refreshcb)
            #  --iup.Append(bind.box,v.cmd)
        for v in bind:
            v.repos()
        bind.dlg.size = nil
        bind.dlg:show()

"""
function formCommand(t,bind,limit,addtobox,profile,refreshcb)
        limit = limit or {}
        local c = limit.cmds or cmds
        -- creat and append the command to the bind.box vbox
        local upactive
        local upbtn = iup.button{title="+";rastersize="20x21"}
        local downbtn = iup.button{title="-";rastersize="20x21"}
        local showhidebtn = iup.button{title="...";rastersize="20x21"}
        local delbtn = iup.button{title="X";rastersize="20x21"}
        t.title = iup.label{title=t.type;rastersize="220x"}
        t.cmd = iup.vbox{iup.hbox{t.title;upbtn;downbtn;showhidebtn;delbtn;alignment="ACENTER"}}
        t.repos = function()
                if bind.order[t] == 1 then upbtn.active = "NO" else upbtn.active = "YES" end
                if bind.order[t] == table.getn(bind) then downbtn.active = "NO" else downbtn.active = "YES" end
        end
        if t.nosettings then showhidebtn.active = "NO" end
        iup.Append(bind.box,t.cmd)
        -- add cmd to the bind.cmd 
        showhidebtn.action = function()
                local destroytarget = nil
                if bind.current == nil then
                        c[t.type].form(t,profile,refreshcb)
                        iup.Append(t.cmd,t.settings)
                        bind.current = t.settings
                elseif bind.current == t.settings then
                        --hide t.
                        iup.Detach(t.settings)
                        destroytarget = t.settings
                        t.settings = nil
                        bind.current = nil
                else
                        -- hide bind.current, then show t.
                        iup.Detach(bind.current)
                        destroytarget = bind.current
                        c[t.type].form(t,profile,refreshcb)
                        iup.Append(t.cmd,t.settings)
                        bind.current = t.settings
                end
                bind.dlg.size = nil
                bind.dlg:show()
                if destroytarget then iup.Destroy(destroytarget) end
        end
        bind.order[t] = table.getn(bind) + 1
        --bind[bind.order[t]] = t
        local found
        for i,v in ipairs(bind) do
                if v == t then found = true break end
        end
        if not found then
                table.insert(bind,t)
        end
        if bind.order[t] - 1 > 0 then
                bind[bind.order[t] - 1].repos()
        end
        t.repos()
        t.title.title = bind.order[t]..": "..t.type
        upbtn.action = function()
                prevt = bind[bind.order[t] - 1]
                bind.order[prevt] = bind.order[t]
                bind.order[t] = bind.order[t] - 1
                bind[bind.order[t]] = t
                bind[bind.order[prevt]] = prevt
                refreshCmds(bind,limit,profile,refreshcb)
                if refreshcb then refreshcb() end
                --t.repos()
                --prevt.repos()
        end
        downbtn.action = function()
                nextt = bind[bind.order[t] + 1]
                bind.order[nextt] = bind.order[t]
                bind.order[t] = bind.order[t] + 1
                bind[bind.order[t]] = t
                bind[bind.order[nextt]] = nextt
                refreshCmds(bind,limit,profile,refreshcb)
                if refreshcb then refreshcb() end
                --t.repos()
                --nextt.repos()
        end
        delbtn.action = function()
                if iup.Alarm("PowerBind","Delete This Command?","No","Yes") == 2 then
                        -- if this is the current command displayed, detach and destroy the t.settings.
                        t.settings = nil
                        iup.Detach(t.cmd)
                        iup.Destroy(t.cmd)
                        table.remove(bind,bind.order[t])
                        refreshCmds(bind,limit,profile,refreshcb)
                        if refreshcb then refreshcb() end
                        --bind.order[t] = nil
                        --bind.dlg.size = nil
                        --bind.dlg:show()
                        --for i,v in ipairs(bind) do v.repos() end
                end
        end
end

function formPowerBinder(bind,limit,profile,refreshcb)
        -- first create the bind.box vbox, the dialog box, and the new command button at the bottom.
        bind.box = iup.vbox{}
        local newbtn = iup.button{title="Add";rastersize="x21"}
        local showbind = iup.button{title="Show Bind Text";rastersize="x21"}
        limit = limit or {}
        local clist = limit.cmdlist or cmdlist
        table.sort(clist)
        local lbtable = {} for i,v in ipairs(clist) do lbtable[i] = v end
        local lbvalue = clist[1]
        lbtable.value = 1
        lbtable.dropdown = "YES"
        lbtable.visible_items = table.getn(clist)
        if table.getn(clist) > 20 then lbtable.visible_items = 20 end
        lbtable.rastersize="172x21"
        local clb = iup.list(lbtable)
        clb.action = function(_,s,i,v)
                if v == 1 then lbvalue = s end
        end
        bind.dlg = iup.dialog{iup.vbox{bind.box;iup.hbox{clb,newbtn,showbind}};title="PowerBinder",maxbox="NO",resize="NO"} --,mdichild="YES",mdiclient=mdiClient
        bind.order = bind.order or {}
        -- if there are any commands in the bind, form them.  Then show the dialog.
        refreshCmds(bind,limit,profile,refreshcb)
        --if table.getn(bind) > 0 then
        --    for i,v in ipairs(bind) do
        --        formCommand(v,bind,limit)
        --    end
        --end
        -- add support for creating new commands by giving the newbtn.action something to do.
        newbtn.action = function()
                local newcmdtype = lbvalue
                if newcmdtype then
                        local t = cmds[newcmdtype].new(profile)
                        formCommand(t,bind,limit,true,profile,refreshcb)
                        if bind.current then
                                iup.Detach(bind.current)
                                iup.Destroy(bind.current)
                        end
                        cmds[newcmdtype].form(t,profile,refreshcb)
                        if t.settings then iup.Append(t.cmd,t.settings) end
                        bind.current = t.settings
                        bind.dlg.size = nil
                        bind.dlg:show()
                        if refreshcb then refreshcb() end
                end
        end
        showbind.action = function()
                iup.Message("Bind Command",cbPBindToString(bind))
        end
        -- then show the dialog.
        bind.dlg:popup(iup.CENTER,iup.CENTER)
end

function cbParsePBString(bind,str,limit,profile)
        limit = limit or {}
        local clist = limit.cmdlist or cmdlist
        local x = "|"
        str = string.gsub(str,"(\\)(.)",function(a,b) return string.format("\\%03i",a:byte())..string.format("\\%03i",b:byte()) end)
        str = string.gsub(str,"|",string.format("\\%03i",x:byte()))
        str = "|"..string.gsub(str,"%$%$","|")
        local i = 0
        for substr in string.gmatch(str,"|([^|]*)") do
                -- convert /xxx's back to their original form.
                substr = string.gsub(substr,"\\%d%d%d",function(z) return string.char(string.sub(z,2,4)) end)
                -- substr is the string to check against all possibilities.
                -- increment i for the next substring
                i = i + 1
                -- then try to find a match in the possibilities in the limit we are given.
                -- first match is accepted, otherwise, the substring becomes a Custom Bind.
                local tab
                for _,v in ipairs(clist) do
                        if cmds[v].match then
                                tab = cmds[v].match(substr,profile)
                                if tab then
                                        break
                                end
                        end
                end
                if not tab then
                        tab = newCustomBind()
                        tab.custom = substr
                end
                table.insert(bind,tab)
        end
end

function newPowerBind(bind,limit,profile)
        local t = bind or {}
        if not (type(t) == "table") then t = {} end
        t.limit = limit or {}
        setmetatable(t,pbindmt)
        if type(bind) == "string" and bind ~= "" then
                cbParsePBString(t,bind,limit,profile)
                --local t2 = newCustomBind()
                --t2.custom = bind
                --formCommand(t2,t,limit,true,profile)
                --t.order = t.order or {}
                --table.insert(t.order,t2)
                --table.insert(t,t2)
        end
        return t
end

local allowedkeys = {[iup.K_INS] = true, [iup.K_HOME] = true, [iup.K_LEFT] = true, [iup.K_RIGHT] = true, [iup.K_END] = true,
        [iup.K_sLEFT] = true, [iup.K_sRIGHT] = true, [iup.K_sHOME] = true, [iup.K_sEND] = true, }

function cbPowerBindBtn(label,t,v,limit,w,h,profile,refreshcb,returncb,bindtostring)
        w = w or 200
        h = h or 21
        w = w - 21
        if not (type(t[v]) == "table") then t[v] = newPowerBind(t[v],limit,profile) end
        local bind = t[v]
        assert(t[v])
        assert(bind)
        bindtostring = bindtostring or cbPBindToString
        local bindtext = iup.text{value=bindtostring(t[v],profile),rastersize=w.."x"..h}
        bindtext.action = function(_,c,s)
                if allowedkeys[c] then return iup.DEFAULT end
                local caret = string.len(s) - _.caret - 1
                bind = {}
                t[v] = bind
                bind.limit = limit or {}
                setmetatable(t[v],pbindmt)
                cbParsePBString(bind,s,limit,profile)
                _.value = cbPBindToString(t[v],profile)
                if c ~= iup.K_BS and c ~= iup.K_DEL then
                        _.caret = string.len(_.value) - caret
                elseif c == iup.K_DEL then
                        _.caret = string.len(_.value) - caret - 1
                else
                        _.caret = string.len(_.value) - caret - 2
                end
                profile.modified = true
                return iup.DEFAULT
        end
        bindtext.getfocus_cb = function(_)
                _.value = cbPBindToString(t[v],profile)
        end
        bindtext.killfocus_cb = function(_)
                _.value = bindtostring(t[v],profile)
        end
        local tbtn = iup.button{title = "..."; rastersize = "21x21", tip = cbTTip}
        tbtn.action = function()
                formPowerBinder(t[v],limit,profile,function()
                        bindtext.value = bindtostring(t[v],profile)
                        if refreshcb then refreshcb() end
                end)
                if type(returncb) == "function" then
                        returncb()
                elseif type(returncb) == "table" and type(returncb.returncb) == "function" then
                        returncb.returncb()
                else
                        cbdlg.bringfront="YES"
                end
        end
        cbTTip = nil
        return iup.hbox{bindtext,tbtn}
end
"""
