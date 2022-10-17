import wx
from pathlib import Path, PureWindowsPath
import json

from BindFile import BindFile
from KeyBind import FileKeyBind
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

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, style = wx.NB_TOP, name = "Profile")

        self.BindFiles = {}
        self.Pages     = []

        # TODO -- here's where we'd load a profile from a file or something.

        # Add the individual tabs, in order.
        self.CreatePage(General(self))
        self.CreatePage(Gameplay(self))
        self.CreatePage(CustomBinds(self))
        self.CreatePage(SoD(self))
        self.CreatePage(InspirationPopper(self))
        self.CreatePage(Mastermind(self))
        #self.CreatePage(ComplexBinds(self))

    def CreatePage(self, module):
        module.BuildPage()
        self.AddPage(module, module.TabTitle)

        modname = type(module).__name__

        setattr(self, modname, module)

        self.Pages.append(modname)

        self.Layout()

    #####
    # Convenience / JIT accessors
    def Name(self)         : return self.General.GetState('Name')
    def Archetype(self)    : return self.General.GetState('Archetype')
    def BindsDir(self)     : return wx.ConfigBase.Get().Read('BindPath')
    def GameBindsDir(self) : return wx.ConfigBase.Get().Read('GameBindPath') or self.BindsDir()
    def ResetFile(self)    : return self.GetBindFile("reset.txt")

    def BLF(self, *args):
        return "$$bindloadfile " + self.BLFPath(*args)

    def BLFPath(self, *args):
        filepath = PureWindowsPath(self.GameBindsDir())
        for arg in args:
            filepath = filepath  /  arg
        return str(filepath)

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

    ###################
    # Profile Save/Load
    def ProfilePath(self):
        return Path.home() / "Documents" / "bindcontrol"

    def ProfileFile(self):
        return Path(self.ProfilePath(), self.Name() + ".bcp")

    def SaveToFile(self, _):

        savefile = self.ProfileFile()

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

        savedata['CustomBinds'] = []

        customPage = getattr(self, 'CustomBinds')
        for pane in customPage.PaneSizer.GetChildren():
            bindpane = pane.GetSizer().GetChildren()[0].GetWindow()
            savedata['CustomBinds'].append(bindpane.Serialize())

        dumpstring = json.dumps(savedata, indent=0)
        try:
            savefile.touch() # make sure there's one there.
            savefile.write_text(dumpstring)
            wx.LogInfo(f"Wrote profile '{savefile}''")
        except Exception as e:
            wx.LogError(f"Problem saving to profile '{savefile}': {e}")

    def LoadFromFile(self, _):

        with wx.FileDialog(self, "Open Profile file",
                wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(self.ProfilePath()),
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogInfo("User canceled loading profile")
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

                    if not value: continue

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

                page.SynchronizeUI()

            cbpage = getattr(self, "CustomBinds")
            for custombind in data['CustomBinds']:
                if custombind['Type'] == "SimpleBind":
                    bindpane = SimpleBindPane(cbpage, init = custombind)
                    cbpage.AddBindToPage(bindpane = bindpane)

            wx.LogInfo(f"Loaded profile {pathname}")

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

        # Start by making reset load itself.  This might get overridden with
        # more elaborate load strings in like SoD, but this is the safety

        config = wx.ConfigBase.Get()
        resetfile = self.ResetFile()
        resetfile.SetBind(FileKeyBind(config.Read('ResetKey'), "Reset Key", "Preferences", resetfile.BLF()))


        # Go to each page....
        for pageName in self.Pages:
            page = getattr(self, pageName)

            # ... and tell it to gather up binds and put them into bindfiles.
            page.PopulateBindFiles()

        # Now we have them here and can iterate them
        errors = donefiles = 0
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

        with DoneDialog(self, msg = msg) as dlg: dlg.ShowModal()

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
                       value = "/bindloadfile " + parent.GameBindsDir() + "reset.txt"
        )
        textCtrl.SetFont(
            wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = u'Courier')
        )

        sizer.Add( textCtrl, 0, wx.EXPAND|wx.ALL, 10)

        sizer.Add( self.CreateButtonSizer(wx.OK), 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizerAndFit(sizer)

