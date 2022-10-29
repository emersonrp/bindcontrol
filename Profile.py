import wx
import re
from pathlib import Path, PureWindowsPath
import json

from BindFile import BindFile

from Page.General import General
from Page.Gameplay import Gameplay
from Page.SoD import SoD
from Page.InspirationPopper import InspirationPopper
from Page.Mastermind import Mastermind
#from Page.ComplexBinds
from Page.CustomBinds import CustomBinds

import UI
from UI.ControlGroup import bcKeyButton
from UI.SimpleBindPane import SimpleBindPane

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
        self.SoD               = self.CreatePage(SoD(self))
        self.InspirationPopper = self.CreatePage(InspirationPopper(self))
        self.Mastermind        = self.CreatePage(Mastermind(self))
        #self.CreatePage(ComplexBinds(self))

        # bind all control events so we can decide that we're modified.
        for evt in [
            wx.EVT_CHECKBOX, wx.EVT_BUTTON, wx.EVT_CHOICE, wx.EVT_COMBOBOX, wx.EVT_TEXT, wx.EVT_SPINCTRL,
            wx.EVT_DIRPICKER_CHANGED, wx.EVT_COLOURPICKER_CHANGED, wx.EVT_MENU,
        ]:
            self.Bind(evt, self.SetModified)

        if loadfile: self.doLoadFromFile(loadfile)

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
        if gbp:
            return PureWindowsPath(gbp) / self.Name()
        else:
            return self.BindsDir()

    def BLF(self, *args):
        filepath = self.GameBindsDir()
        for arg in args: filepath = filepath  /  arg
        return "$$bindloadfilesilent " + str(filepath)

    def CheckConflict(self, key, button):
        conflicts = []

        for pageName in self.Pages:
            page = getattr(self, pageName)
            for ctrlname, ctrl in page.Ctrls.items():
                if not ctrl.IsThisEnabled(): continue
                if ctrl == button: continue
                if isinstance(ctrl, bcKeyButton):
                    if key == ctrl.GetLabel():
                        conflicts.append( {'page' : pageName, 'ctrl': UI.Labels[ctrlname]})
        return conflicts

    def SetModified  (self, _ = None): self.Modified = True
    def ClearModified(self, _ = None): self.Modified = False

    ###################
    # Profile Save/Load
    def ProfilePath(self):
        return Path.home() / "Documents" / "bindcontrol"

    def SaveToFile(self, _ = None):
        with wx.FileDialog(self, "Save Profile file",
                wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(self.ProfilePath()),
                defaultFile = self.Name() + '.bcp',
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogMessage("User canceled saving new profile")
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            if not re.search(r'\.bcp$', pathname):
                pathname = pathname + '.bcp'
            self.Filename = Path(pathname)

            return self.doSaveToFile()

    def doSaveToFile(self, _ = None):
        savefile = self.Filename
        if not savefile:
            return self.SaveToFile()

        profilename = self.General.GetState('Name')
        if len(profilename) == 0 or re.search(" ", profilename):
            wx.MessageBox("Profile Name is not valid, please correct this.")
            self.ChangeSelection(0)
            return

        self.ProfilePath().mkdir( parents = True, exist_ok = True )

        savedata = {}
        for pagename in self.Pages:
            savedata[pagename] = {}
            if pagename == "CustomBinds": continue

            page = getattr(self, pagename)
            for controlname, control in page.Ctrls.items():
                # skip if off
                if control.IsEnabled():
                    # look up what type of control it is to know how to extract its value
                    controlType = type(control).__name__
                    if controlType == 'DirPickerCtrl':
                        value = control.GetPath()
                    elif controlType == 'Button' or controlType == 'bcKeyButton':
                        value = control.GetLabel()
                    elif controlType == 'ColourPickerCtrl':
                        value = control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
                    elif controlType == 'Choice':
                        value = control.GetSelection()
                    elif controlType == 'StaticText':
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
            bindpane = pane.GetSizer().GetChildren()[0].GetWindow()
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
                wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(self.ProfilePath()),
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogMessage("User canceled loading profile")
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.doLoadFromFile(pathname)

    def doLoadFromFile(self, pathname):
        with Path(pathname) as file:
            datastring = file.read_text()
            data = json.loads(datastring)

            for pagename in self.Pages:
                if pagename == "CustomBinds": continue
                page = getattr(self, pagename)
                for controlname, control in page.Ctrls.items():
                    value = data[pagename].get(controlname, None)

                    if value == None: continue

                    # look up what type of control it is to know how to extract its value
                    controlType = type(control).__name__
                    if controlType == 'DirPickerCtrl':
                        control.SetPath(value)
                    elif controlType == 'Button' or controlType == 'bcKeyButton':
                        control.SetLabel(value)
                    elif controlType == 'ColourPickerCtrl':
                        control.SetColour(value)
                    elif controlType == 'Choice':
                        control.SetSelection(value)
                    else:
                        control.SetValue(value)

                if pagename == 'General':
                    page.IncarnateBox.FillWith(data)
                    # Re-fill Primary and Secondary pickers.
                    page.OnPickArchetype()
                    page.Ctrls['Primary']  .SetSelection(data['General'].get('Primary'  , None))
                    page.Ctrls['Secondary'].SetSelection(data['General'].get('Secondary', None))
                else:
                    page.SynchronizeUI()  # this clears and repops the Primary and Secondary pickers on 'General'

            cbpage = getattr(self, "CustomBinds")
            for custombind in data['CustomBinds']:
                if not custombind: continue
                if custombind['Type'] == "SimpleBind":
                    bindpane = SimpleBindPane(cbpage, init = custombind)
                    cbpage.AddBindToPage(bindpane = bindpane)

            self.Filename = Path(pathname)
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
        # more elaborate load strings in like SoD, but this is the safety

        config = wx.ConfigBase.Get()
        resetfile = self.ResetFile()
        keybindreset = 'keybind_reset$$' if config.ReadBool('FlushAllBinds') else ''
        resetfile.SetBind(config.Read('ResetKey'), "Reset Key", "Preferences", keybindreset + resetfile.BLF())


        errors = donefiles = 0
        #
        # Go to each page....
        for pageName in self.Pages:
            page = getattr(self, pageName)

            # ... and tell it to gather up binds and put them into bindfiles.
            try:
                page.PopulateBindFiles()
            except Exception as e:
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
                wx.LogError(f"Failed to write bindfile {filename}: {e}")
                donefiles -= 1
                errors += 1

            dlg.Update(donefiles, filename)

        dlg.Destroy()

        if errors:
            msg = f"{donefiles} bind files written, but there were {errors} errors.  Check the log."
        else:
            msg = f"{donefiles} bind files written!"

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

        msg = msg + "\n\nLog on to the character you made these for and type:"

        sizer.Add(
            wx.StaticText(self, label = msg, style = wx.ALIGN_CENTER),
            1, wx.EXPAND|wx.ALL, 10
        )
        textCtrl = wx.TextCtrl(self, id = wx.ID_ANY,
                       style = wx.TE_READONLY|wx.TE_CENTER,
                       value = "/bindloadfilesilent " + str(parent.GameBindsDir() / "reset.txt")
        )
        textCtrl.SetFont(
            wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = u'Courier')
        )

        sizer.Add( textCtrl, 0, wx.EXPAND|wx.ALL, 10)

        sizer.Add( self.CreateButtonSizer(wx.OK), 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizerAndFit(sizer)

