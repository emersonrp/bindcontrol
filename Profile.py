import re
from pathlib import Path, PureWindowsPath
from typing import Dict, Any
import json
import wx
import wx.lib.colourselect as csel

from BindFile import BindFile
from BLF import BLF

from Page.General import General
from Page.Gameplay import Gameplay
from Page.MovementPowers import MovementPowers
from Page.InspirationPopper import InspirationPopper
from Page.Mastermind import Mastermind
from Page.CustomBinds import CustomBinds

import UI
from UI.ControlGroup import cgStaticText, cgSpinCtrl, cgSpinCtrlDouble
from UI.SimpleBindPane import SimpleBindPane
from UI.BufferBindPane import BufferBindPane
from UI.ComplexBindPane import ComplexBindPane
from UI.KeySelectDialog import bcKeyButton

class Profile(wx.Notebook):

    def __init__(self, parent, loadfile = None):
        wx.Notebook.__init__(self, parent, style = wx.NB_TOP, name = "Profile")

        self.BindFiles : dict      = {}
        self.Pages     : list      = []
        self.Modified  : bool      = False
        self.Filename  : Path|None = None

        # Add the individual tabs, in order.
        self.General           = self.CreatePage(General(self))
        self.Gameplay          = self.CreatePage(Gameplay(self))
        self.CustomBinds       = self.CreatePage(CustomBinds(self))
        self.MovementPowers    = self.CreatePage(MovementPowers(self))
        self.InspirationPopper = self.CreatePage(InspirationPopper(self))
        self.Mastermind        = self.CreatePage(Mastermind(self))

        # bind all control events so we can decide that we're modified.
        for evt in [
            wx.EVT_CHECKBOX, wx.EVT_BUTTON, wx.EVT_CHOICE, wx.EVT_COMBOBOX, wx.EVT_TEXT, wx.EVT_SPINCTRL,
            wx.EVT_DIRPICKER_CHANGED, wx.EVT_COLOURPICKER_CHANGED, wx.EVT_MENU,
        ]:
            self.Bind(evt, self.SetModified)

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChanged)

        if loadfile: self.doLoadFromFile(loadfile)

    def onPageChanged(self, evt):
        scrollpane = self.Parent
        if (evt.GetSelection() == 2): # TODO this is ugly hard-coded for "Custom Binds" tab
            scrollpane.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)
            scrollpane.Bind(wx.EVT_SCROLLWIN, self.doNothing)
            scrollpane.SetVirtualSize(scrollpane.GetClientSize())
        else:
            scrollpane.ShowScrollbars(wx.SHOW_SB_DEFAULT, wx.SHOW_SB_DEFAULT)
            scrollpane.Bind(wx.EVT_SCROLLWIN, None)
            scrollpane.SetVirtualSize(scrollpane.GetBestVirtualSize())

    def doNothing(self, _): pass

    def CreatePage(self, module):
        module.BuildPage()
        self.AddPage(module, module.TabTitle)

        modname = type(module).__name__

        self.Pages.append(modname)

        self.Layout()
        return module

    #####
    # Convenience / JIT accessors
    def Name(self)         : return self.General.GetState('Name')
    def Archetype(self)    : return self.General.GetState('Archetype')
    def ResetFile(self)    : return self.GetBindFile("reset.txt")
    def BindsDir(self)     :
        return Path(wx.ConfigBase.Get().Read('BindPath')) / self.Name()
    def GameBindsDir(self) :
        gbp = wx.ConfigBase.Get().Read('GameBindPath')
        if gbp: return PureWindowsPath(gbp) / self.Name()
        return self.BindsDir()

    def HasPowerPool(self, poolname):
        for picker in ['Pool1', 'Pool2', 'Pool3', 'Pool4']:
            if self.General.Ctrls[picker].GetString(self.General.Ctrls[picker].GetSelection()) == poolname:
                return True
        return False

    def BLF(self, *args):
        filepath = self.GameBindsDir()
        for arg in args: filepath = filepath  /  arg
        return f"$${BLF()} " + str(filepath)

    def CheckConflict(self, key, existingctrlname):
        conflicts = []

        for pageName in self.Pages:
            page = getattr(self, pageName)
            for ctrlname, ctrl in page.Ctrls.items():
                if not ctrl.IsThisEnabled(): continue
                if isinstance(ctrl, bcKeyButton):
                    if key == ctrl.Key and not existingctrlname == ctrlname:
                        conflicts.append( {'page' : page.TabTitle, 'ctrl': UI.Labels[ctrlname]})
        return conflicts

    def SetModified  (self, _ = None): self.Modified = True
    def ClearModified(self, _ = None): self.Modified = False

    ###################
    # Profile Save/Load
    def ProfilePath(self):
        return Path(wx.ConfigBase.Get().Read('ProfilePath'))

    def SaveAsDefault(self, _ = None):
        currentfilename = self.Filename
        currentmodified = self.Modified
        currentname     = self.Name()

        self.General.SetState('Name', 'Default')
        self.Filename = Path(self.ProfilePath() / 'Default.bcp')

        if self.Filename.exists():
            result = wx.MessageBox("Overwrite Default Profile?", "Profile Exists", wx.YES_NO)
            if result == wx.NO: return

        self.doSaveToFile()

        self.Filename = currentfilename
        self.Modified = currentmodified
        self.General.SetState('Name', currentname)

    def SaveToFile(self, _ = None):
        try:
            self.ProfilePath().mkdir( parents = True, exist_ok = True )
        except Exception as e:
            wx.LogError(f"Can't make Profile path {self.ProfilePath()} - {e}")

        with wx.FileDialog(self, "Save Profile file",
                wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(self.ProfilePath()),
                defaultFile = self.Name() + '.bcp',
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogMessage("User canceled saving new profile")
                return False    # the user changed their mind

            # Proceed with the file chosen by the user
            pathname = fileDialog.GetPath()
            if not re.search(r'\.bcp$', pathname):
                pathname = pathname + '.bcp'

            self.Filename = Path(pathname)
            self.General.SetState('Name', self.Filename.stem)

            return self.doSaveToFile()

    def doSaveToFile(self, _ = None):
        if not self.Filename:
            return self.SaveToFile()

        profilename = self.General.GetState('Name')
        if len(profilename) == 0 or re.search(" ", profilename):
            wx.MessageBox("Profile Name is not valid, please correct this.")
            self.ChangeSelection(0)
            return False

        self.ProfilePath().mkdir( parents = True, exist_ok = True )

        self.Filename = self.ProfilePath() / Path(profilename + ".bcp")
        savefile = self.Filename

        savedata : Dict[str, Any] = {}
        for pagename in self.Pages:
            savedata[pagename] = {}
            if pagename == "CustomBinds": continue

            page = getattr(self, pagename)
            for controlname, control in page.Ctrls.items():
                # Save disabled controls' states, too, so as not to lose config
                # if someone, say, turns on "disable self tell" with a bunch of custom colors defined
                # look up what type of control it is to know how to extract its value
                if isinstance(control, wx.DirPickerCtrl):
                    value = control.GetPath()
                elif isinstance(control, bcKeyButton):
                    value = control.Key
                elif isinstance(control, wx.Button):
                    value = control.GetLabel()
                elif isinstance(control, wx.ColourPickerCtrl) or isinstance(control, csel.ColourSelect):
                    value = control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
                elif isinstance(control, wx.Choice):
                    # we used to save the numerical selection which could break if the contents
                    # of a picker changed between runs, like, say, if new powersets appeared.
                    # Save the string value instead
                    value = ""
                    sel = control.GetSelection()
                    if (sel != wx.NOT_FOUND): value = control.GetString(sel)
                elif isinstance(control, wx.StaticText):
                    continue
                else:
                    value = control.GetValue()

                savedata[pagename][controlname] = value

            if pagename == "General":
                incarnatedata = page.IncarnateBox.GetData()
                if incarnatedata:
                    savedata[pagename]['Incarnate'] = incarnatedata


        savedata['CustomBinds'] = []
        customPage = getattr(self, 'CustomBinds')
        for pane in customPage.PaneSizer.GetChildren():
            bindui = pane.GetSizer().GetChildren()
            if bindui:
                bindpane = bindui[0].GetWindow()
                if bindpane:
                    savedata['CustomBinds'].append(bindpane.Serialize())

        dumpstring = json.dumps(savedata, indent=2)
        try:
            wx.ConfigBase.Get().Write('LastProfile', str(savefile))
            savefile.touch() # make sure there's one there.
            savefile.write_text(dumpstring)
            wx.LogMessage(f"Wrote profile '{savefile}'")
            self.ClearModified()
        except Exception as e:
            wx.LogError(f"Problem saving to profile '{savefile}': {e}")

    def LoadFromFile(self, _):
        with wx.FileDialog(self, "Open Profile file",
                wildcard   = "Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(self.ProfilePath()),
                style      = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogMessage("User canceled loading profile")
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.doLoadFromFile(pathname)

    def doLoadFromFile(self, pathname):
        with Path(pathname) as file:
            try:
                datastring = file.read_text()
            except Exception as e:
                wx.LogError(f"Profile {pathname} could not be loaded: {e}")
                return None

            data = json.loads(datastring)

            # load old Profiles pre-rename
            if 'SoD' in data: data['MovementPowers'] = data['SoD']

            for pagename in self.Pages:
                if pagename == "CustomBinds": continue
                page = getattr(self, pagename)
                for controlname, control in page.Ctrls.items():

                    value = None
                    if pagename in data:
                        if controlname in data[pagename]:
                            value = data[pagename].get(controlname, None)
                        # if we don't have a given control in the load data, skip it completely --
                        # it should already have the default value from Init
                        else: continue

                    # look up what type of control it is to know how to update its value
                    if isinstance(control, wx.DirPickerCtrl):
                        control.SetPath(value if value else '')
                    elif isinstance(control, bcKeyButton):
                        control.SetLabel(value if value else '')
                        control.Key = value if value else ''
                    elif isinstance(control, wx.Button):
                        control.SetLabel(value if value else '')
                    elif isinstance(control, wx.ColourPickerCtrl) or isinstance(control, csel.ColourSelect):
                        control.SetColour(value)
                        if isinstance(control, csel.ColourSelect):
                            wx.PostEvent(control, wx.CommandEvent(csel.EVT_COLOURSELECT.typeId, control.GetId()))
                    elif isinstance(control, wx.Choice):
                        # we used to save the numerical selection which could break if the contents
                        # of a picker changed between runs, like, say, if new powersets appeared.
                        # we still check whether we have a numerical value so we can load old profiles.
                        if isinstance(value, str):
                            value = control.FindString(value)
                            if value == wx.NOT_FOUND: value = 0
                        control.SetSelection(value if value else 0)
                    elif isinstance(control, wx.CheckBox):
                        control.SetValue(value if value else False)
                    elif isinstance(control, cgStaticText):
                        continue
                    elif isinstance(control, cgSpinCtrl) or isinstance(control, cgSpinCtrlDouble):
                        control.SetValue(value if value else page.Init.get(controlname, 0))
                    else:
                        control.SetValue(value if value else '')

                if pagename == 'General':
                    page.IncarnateBox.FillWith(data)
                    # Re-fill Primary and Secondary pickers, honoring old numeric indices if needed
                    page.OnPickArchetype()
                    prim = data['General'].get('Primary', None)
                    if isinstance(prim, str):
                        prim = page.Ctrls['Primary'].FindString(prim)
                    page.Ctrls['Primary']  .SetSelection(prim)

                    seco = data['General'].get('Secondary', None)
                    if isinstance(seco, str):
                        seco = page.Ctrls['Secondary'].FindString(seco)
                    page.Ctrls['Secondary'].SetSelection(seco)

                    epic = data['General'].get('Epic', None)
                    if isinstance(epic, str):
                        epic = page.Ctrls['Epic'].FindString(epic)
                    page.Ctrls['Epic'].SetSelection(epic)
                else:
                    page.SynchronizeUI()  # this clears/repops the Primary/Secondary pickers on 'General' so don't do it there

            cbpage = getattr(self, "CustomBinds")
            if cbpage:
                cbpage.scrolledPanel.DestroyChildren()
                cbpage.Ctrls = []
                cbpage.Panes = []
                for custombind in data['CustomBinds']:
                    if not custombind: continue

                    bindpane = None
                    if custombind['Type'] == "SimpleBind":
                        bindpane = SimpleBindPane(cbpage, init = custombind)
                    elif custombind['Type'] == "BufferBind":
                        bindpane = BufferBindPane(cbpage, init = custombind)
                    elif custombind['Type'] == "ComplexBind":
                        bindpane = ComplexBindPane(cbpage, init = custombind)

                    if bindpane:
                        cbpage.AddBindToPage(bindpane = bindpane)

            self.Filename = Path(pathname)
            wx.ConfigBase.Get().Write('LastProfile', str(file))
            wx.ConfigBase.Get().Flush()
            wx.LogMessage(f"Loaded profile {pathname}")
            self.ClearModified()

    #####################
    # Bind file functions
    def GetBindFile(self, *filename):
        # Store them internally as a simple string
        # but send BindFile the list of path parts
        filename_key = "!!".join(filename)

        if not self.BindFiles.get(filename_key, None):
            self.BindFiles[filename_key] = BindFile(self, *filename)

        return self.BindFiles[filename_key]


    def WriteBindFiles(self):

        profilename = self.General.GetState('Name')
        if len(profilename) == 0 or re.search(" ", profilename):
            wx.MessageBox("Profile Name is not valid, please correct this.")
            self.ChangeSelection(0)
            return

        # Start by making reset load itself.  This might get overridden with
        # more elaborate load strings in like MovementPowers, but this is the safety

        config = wx.ConfigBase.Get()
        resetfile = self.ResetFile()
        keybindreset = 'keybind_reset' if config.ReadBool('FlushAllBinds') else ''
        feedback = 't $name, Resetting keybinds.'
        resetfile.SetBind(config.Read('ResetKey'), "Reset Key", "Preferences", [keybindreset , feedback, resetfile.BLF()])

        errors = donefiles = 0
        #
        # Go to each page....
        for pageName in self.Pages:
            page = getattr(self, pageName)

            # ... and tell it to gather up binds and put them into bindfiles.
            try:
                page.PopulateBindFiles()
            except Exception as e:
                if config.ReadBool('CrashOnBindError'):
                    raise e
                else:
                    wx.LogError(f"Error populating bind file: {e}")
                    errors += 1

        # Now we have them here and can iterate them
        totalfiles = len(self.BindFiles)
        dlg = wx.ProgressDialog('Writing Bind Files','',
            maximum = totalfiles, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)

        for filename, bindfile in self.BindFiles.items():
            try:
                donefiles += 1
                bindfile.Write()
            except Exception as e:
                if config.ReadBool('CrashOnBindError'):
                    raise e
                else:
                    wx.LogError(f"Failed to write bindfile {filename}: {e}")
                    donefiles -= 1
                    errors += 1

            dlg.Update(donefiles, filename)

        dlg.Destroy()

        if errors:
            msg = f"{donefiles} of {totalfiles} bind files written, but there were {errors} errors.  Check the log."
        else:
            msg = f"{donefiles} of {totalfiles} bind files written successfully."

        with DoneDialog(self, msg = msg) as dlg:

            dlg.ShowModal()
            if errors:
                wx.App.Get().Main.LogWindow.Show()

        # clear out our state
        self.BindFiles = {}


class DoneDialog(wx.Dialog):
    def __init__(self, parent, msg = ''):
        wx.Dialog.__init__(self, parent, title = "Bindfiles Written")

        sizer = wx.BoxSizer(wx.VERTICAL)

        msg = msg + (
            "\n\n"
            "If you are updating existing installed BindControl binds, you can\n"
            f"press \"{wx.ConfigBase.Get().Read('ResetKey')}\" to load your new binds.\n"
            "\n"
            "If this is a new set of keybinds, log on to the character\n"
            "you made them for and type into the chat window:\n"
        )

        sizer.Add(
            wx.StaticText(self, label = msg, style = wx.ALIGN_CENTER),
            1, wx.EXPAND|wx.ALL, 10
        )
        textCtrl = wx.TextCtrl(self, id = wx.ID_ANY,
                       style = wx.TE_READONLY|wx.TE_CENTER,
                       value = "/bindloadfile " + str(parent.GameBindsDir() / "reset.txt")
        )
        textCtrl.SetFont(
            wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = 'Courier')
        )
        sizer.Add( textCtrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        sizer.Add( self.CreateButtonSizer(wx.OK), 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizerAndFit(sizer)
