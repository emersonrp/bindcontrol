import wx
from pathlib import Path
import json

from BindFile import BindFile
from Page.General import General
from Page.Gameplay import Gameplay
from Page.SoD import SoD
from Page.InspirationPopper import InspirationPopper
from Page.Mastermind import Mastermind
#from Page.ComplexBinds
from Page.CustomBinds import CustomBinds

class Profile(wx.Notebook):

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, style = wx.NB_TOP, name = "Profile")

        self.BindFiles = {}
        self.Pages     = []

        # TODO -- here's where we'd load a profile from a file or something.

        # Add the individual tabs, in order.
        self.CreatePage(General(self))
        self.CreatePage(Gameplay(self))
        self.CreatePage(SoD(self))
        self.CreatePage(InspirationPopper(self))
        self.CreatePage(Mastermind(self))
        #self.CreatePage(ComplexBinds(self))
        self.CreatePage(CustomBinds(self))

    def CreatePage(self, module):
        module.BuildPage()
        page = self.AddPage(module, module.TabTitle)

        modname = type(module).__name__

        setattr(self, modname, module)

        self.Pages.append(modname)

        self.Layout()

    #####
    # Convenience / JIT accessors
    def Name(self)         : return self.General.GetState('Name')
    def BindsDir(self)     : return self.General.GetState('BindsDir')
    def GameBindsDir(self) : return (self.General.GetState('GameBindsDir') or self.BindsDir())
    def ProfileFile(self)  : return Path(self.BindsDir(), self.Name() + ".bcp")
    def ResetFile(self)    : return self.GetBindFile("reset.txt")

    ###################
    # Profile Save/Load
    def SaveToFile(self, event):

        savefile = Path(self.ProfileFile())

        savedata = {}
        for pagename in self.Pages:
            savedata[pagename] = {}
            page = getattr(self, pagename)
            for controlname, control in page.Ctrls.items():

                # skip if off
                if control.IsEnabled():

                    # look up what type of control it is to know how to extract its value
                    controlType = type(control).__name__
                    if controlType == 'DirPickerCtrl':
                        value = control.GetPath()
                    elif controlType == 'Button':
                        value = control.GetLabel()
                    elif controlType == 'ColourPickerCtrl':
                        value = control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
                    else:
                        value = control.GetValue()

                    savedata[pagename][controlname] = value

        dumpstring = json.dumps(savedata, indent=0)
        try:
            savefile.touch() # make sure there's one there.
            savefile.write_text(dumpstring)
            # wx.LogError(f"Wrote file {savefile}")
        except None:
            wx.LogError(f"Problem saving to file '{savefile}'")

    def LoadFromFile(self, event):

        with wx.FileDialog(self, "Open Profile file",
               wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
               # wildcard="Bindcontrol and Citybinder Profiles (*.bcp;*.cbp)|*.bcp;*.cbp",
               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            with Path(pathname) as file:
                try:
                    datastring = file.read_text()
                    data = json.loads(datastring)

                    for pagename in self.Pages:
                        page = getattr(self, pagename)
                        for controlname, control in page.Ctrls.items():
                            value = data[pagename][controlname]

                            # look up what type of control it is to know how to extract its value
                            controlType = type(control).__name__
                            if controlType == 'DirPickerCtrl':
                                control.SetPath(value)
                            elif controlType == 'Button':
                                control.SetLabel(value)
                            elif controlType == 'ColourPickerCtrl':
                                control.SetColour(value)
                            else:
                                control.SetValue(value)

                except:
                    wx.LogError("Cannot open file '%s'." % file)

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
        # Go to each page....
        for pageName in self.Pages:
            page = getattr(self, pageName, None)

            # ... and tell it to gather up binds and put them into bindfiles.
            page.PopulateBindFiles()

        # Now we have them here and can iterate them
        errors = 0
        for filename, bindfile in self.BindFiles.items():
            try:
                bindfile.Write()
            except Exception as e:
                print(f"Done blowed up in bindfile.Write(): {e}")
                errors = errors + 1

        if errors:
            msg = f"Bind files written, but with {errors} errors.  Check the log."
        else:
            msg = "Bind files written!"

        wx.MessageBox(msg, '', wx.OK, self)

        # TODO try except finally
        # clear out our state
        self.BindFiles = {}
