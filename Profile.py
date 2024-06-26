import re
from pathlib import PurePath, Path, PureWindowsPath
from typing import Dict, Any
import json
import codecs
import base64
import wx
import wx.lib.colourselect as csel

from BindFile import BindFile
from BLF import BLF

from Icon import GetIcon

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

        if loadfile: self.doLoadFromFile(loadfile)

    def CreatePage(self, module):
        module.BuildPage()
        module.SetScrollRate(10,10)
        self.AddPage(module, module.TabTitle)

        modname = type(module).__name__

        self.Pages.append(modname)

        self.Layout()
        return module

    #####
    # Convenience / JIT accessors
    def Name(self)         : return self.General.GetState('Name')
    def Archetype(self)    : return self.General.GetState('Archetype')
    def Primary(self)      : return self.General.GetState('Primary')
    def Secondary(self)    : return self.General.GetState('Secondary')
    def ResetFile(self)    : return self.GetBindFile("reset.txt")
    def BindsDir(self)     :
        return Path(wx.ConfigBase.Get().Read('BindPath')) / self.Name()
    def GameBindsDir(self) :
        gbp = wx.ConfigBase.Get().Read('GameBindPath')
        if gbp: return PureWindowsPath(gbp) / self.Name()
        return self.BindsDir()

    def HasPowerPool(self, poolname):
        for picker in ['Pool1', 'Pool2', 'Pool3', 'Pool4']:
            pctrl = self.General.Ctrls[picker]
            if pctrl.GetString(pctrl.GetSelection()) == poolname:
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
                if isinstance(ctrl, bcKeyButton):
                    if not ctrl.IsThisEnabled(): continue
                    if (key != '') and (key == ctrl.Key) and (not existingctrlname == ctrlname):
                        conflicts.append( {'page' : page.TabTitle, 'ctrl': UI.Labels[ctrlname]})
        return conflicts

    # check all buttons for conflicts.
    def CheckAllConflicts(self):
        for pageName in self.Pages:
            page = getattr(self, pageName)
            for _, ctrl in page.Ctrls.items():
                if isinstance(ctrl, bcKeyButton):
                    if not ctrl.IsThisEnabled(): continue
                    ctrl.CheckConflicts()


    def SetModified  (self, _ = None): self.Modified = True
    def ClearModified(self, _ = None): self.Modified = False

    ###################
    # Profile Save/Load
    def ProfilePath(self):
        return Path(wx.ConfigBase.Get().Read('ProfilePath'))

    def SaveAsDefault(self, prompt = True):
        if prompt:
            result = wx.MessageBox("This will set the current profile to be used as a template when making a new profile.  Continue?", "Save As Default", wx.YES_NO)
            if result == wx.NO: return

        # stash away our current values
        currName = self.Name()
        filename = self.Filename
        self.Freeze()
        try:
            # so much could go wrong.
            self.General.SetState('Name', '')
            self.Filename = None
            jsonstring = self.AsJSON(small = True)
            zipstring = codecs.encode(jsonstring.encode('utf-8'), 'zlib')
            b64string = base64.b64encode(zipstring)

            wx.ConfigBase.Get().Write('DefaultProfile', b64string)
            wx.ConfigBase.Get().Flush()
        except Exception as e:
            # Let us know if it did
            wx.LogError(f"Failed to write default profile: {e}")
        finally:
            # clean up our stashed state
            self.General.SetState('Name', currName)
            self.Filename = filename
            self.Thaw()

    def GetDefaultProfileJSON(self, _ = None):
        jsonstring = None

        # If we have it already saved the new way
        if wx.ConfigBase.Get().HasEntry('DefaultProfile'):
            try:
                b64string = wx.ConfigBase.Get().Read('DefaultProfile')
                zipstring = base64.b64decode(b64string)
                jsonstring = codecs.decode(zipstring, 'zlib')
            except Exception as e:
                wx.LogError(f"Problem loading default profile: {e}")

        return jsonstring

    def LoadFromDefault(self, _ = None):
        FoundOldDefaultProfile = False
        # Try to get it from prefs
        jsonstring = self.GetDefaultProfileJSON()
        if not jsonstring:
            # Otherwise look for the file way
            oldDefaultProfile = self.ProfilePath() / "Default.bcp"
            if oldDefaultProfile.exists():
                FoundOldDefaultProfile = True
                jsonstring = oldDefaultProfile.read_text()

        self.doLoadFromJSON(jsonstring)

        # if we found one the file way, migrate it to the new way
        if FoundOldDefaultProfile:
            self.SaveAsDefault(prompt = False)

    def SaveToFile(self, _ = None):
        try:
            self.ProfilePath().mkdir( parents = True, exist_ok = True )
        except Exception as e:
            wx.LogError(f"Can't make Profile path {self.ProfilePath()} - {e}.  Aborting Save.")
            return

        with wx.FileDialog(self, "Save Profile file",
                wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
                defaultDir = str(self.ProfilePath()),
                defaultFile = self.Name(),
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                wx.LogMessage("User canceled saving new profile")
                return False    # the user changed their mind

            # Proceed with the file chosen by the user
            pathname = fileDialog.GetPath()
            if not re.search(r'\.bcp$', pathname, flags = re.I):
                pathname = pathname + '.bcp'

            self.Filename = Path(pathname)
            self.General.SetState('Name', self.Filename.stem)

            return self.doSaveToFile()

    def doSaveToFile(self, _ = None):
        if not self.Filename:
            return self.SaveToFile()

        profilename = self.Name()
        if len(profilename) == 0 or re.search(" ", profilename):
            wx.MessageBox("Profile Name is not valid, please correct this.")
            self.ChangeSelection(0)
            return False

        self.ProfilePath().mkdir( parents = True, exist_ok = True )

        #self.Filename = self.ProfilePath() / Path(profilename + ".bcp")
        if not self.Filename:
            raise Exception(f"No Filename set in Profile {self.Name()}!  Aborting save.")
        savefile = self.Filename

        dumpstring = self.AsJSON()

        try:
            wx.ConfigBase.Get().Write('LastProfile', str(savefile))
            savefile.touch() # make sure there's one there.
            savefile.write_text(dumpstring)
            wx.LogMessage(f"Wrote profile {savefile}")
            self.ClearModified()
        except Exception as e:
            wx.LogError(f"Problem saving to profile {savefile}: {e}")

    def AsJSON(self, small = False):
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

        if small:
            return json.dumps(savedata, separators = (',', ':'))
        else:
            return json.dumps(savedata, indent=2)

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
                jsonstring = file.read_text()
                self.doLoadFromJSON(jsonstring)
            except Exception as e:
                wx.LogError(f"Profile {pathname} could not be loaded: {e}")
                return None

        self.Filename = Path(pathname)
        wx.ConfigBase.Get().Write('LastProfile', pathname)
        wx.ConfigBase.Get().Flush()
        wx.LogMessage(f"Loaded profile {pathname}")

    def doLoadFromJSON(self, jsonstring):
        if not jsonstring: return

        data = json.loads(jsonstring)

        # load old Profiles pre-rename of "Movement Powers" tab
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

            page.SynchronizeUI()

            # Do this after SynchronizeUI for General because SynchronizeUI will blow away our powerset
            # picks when we re-fill those pickers from the archetype.
            if pagename == 'General':
                page.IncarnateBox.FillWith(data)
                # Re-fill Primary and Secondary pickers, honoring old numeric indices if needed
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

        cbpage = getattr(self, "CustomBinds")
        if cbpage:
            cbpage.scrolledPanel.DestroyChildren()
            cbpage.Ctrls = {}
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
        self.ClearModified()


    #####################
    # Bind file functions
    def GetBindFile(self, *filebits):
        filepath = PurePath(*filebits)
        key = str(filepath)

        if not self.BindFiles.get(key, None):
            self.BindFiles[key] = BindFile(self, filepath)

        return self.BindFiles[key]


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

        errors = 0
        donefiles = 0

        # Go to each page....
        for pageName in self.Pages:
            page = getattr(self, pageName)

            # ... and tell it to gather up binds and put them into bindfiles.
            try:
                success = page.PopulateBindFiles()
                if not success:
                    wx.LogError(f'An error on the "{pageName}" tab caused WriteBinds to fail.')
                    return
            except Exception as e:
                if config.ReadBool('CrashOnBindError'):
                    raise e
                else:
                    wx.LogMessage(f"Error populating bind file: {e}")
                    errors += 1

        # Now we have them here and can iterate them
        totalfiles = len(self.BindFiles)
        dlg = wx.ProgressDialog('Writing Bind Files','',
            maximum = totalfiles, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)

        for bindfile in self.BindFiles.values():
            try:
                bindfile.Write()
                donefiles += 1
            except Exception as e:
                if config.ReadBool('CrashOnBindError'):
                    raise e
                else:
                    wx.LogMessage(f"Failed to write bindfile {bindfile.Path}: {e}")
                    errors += 1

            dlg.Update(donefiles, str(bindfile.Path))

        dlg.Destroy()

        if errors:
            msg = f"{donefiles} of {totalfiles} bind files written, but there were {errors} errors.  Check the log."
        else:
            msg = f"{donefiles} of {totalfiles} bind files written successfully."

        with WriteDoneDialog(self, msg = msg) as dlg:
            dlg.ShowModal()
            if errors:
                wx.App.Get().Main.LogWindow.Show()

        # clear out our state
        self.BindFiles = {}

    def AllBindFiles(self):
        files = [self.ResetFile()]
        dirs  = []
        for pageName in self.Pages:
            page = getattr(self, pageName)
            bf = page.AllBindFiles()
            for file in bf['files']:
                files.append(file)
            for bdir in bf['dirs']:
                dirs.append(bdir)

        return {
            'files' : files,
            'dirs'  : dirs,
        }

    def DeleteBindFiles(self):
        result = wx.MessageBox((
                "DELETING ALL BINDFILES"
                "\n\n"
                "This will delete all BindControl-generated files and directories inside:"
                "\n\n"
                f"          {self.BindsDir()}"
                "\n\n"
                "Please double-check this path and make sure this is what you mean to do."
                "\n\n"
                "Are you sure?"
            ), "DELETE ALL BINDFILES", wx.YES_NO)
        if result == wx.NO: return

        removed = self.doDeleteBindFiles(self.AllBindFiles())

        if removed:
            with DeleteDoneDialog(self, removed = removed) as dlg:
                dlg.ShowModal()

    def doDeleteBindFiles(self, bindfiles):

        bindpath = wx.ConfigBase.Get().Read('BindPath')
        if len(bindpath) < 6: # "C:\COH" being the classic
            wx.MessageBox(f"Your Binds Directory is set to '{bindpath}' which seems wrong.  Check the preferences dialog.", "Binds Directory Error", wx.OK)
            return

        if not bindfiles:
            wx.LogError("Tried to doDeleteBindFiles with no bindfiles.  Please report this as a bug.  Bailing.")
            return

        # bindfiles is generated using someone's AllBindFiles(), which uses
        # Profile.GetBindFile(), so if BindsDir is sane, we're probably OK.

        totalfiles = len(bindfiles['files']) + len(bindfiles['dirs'])
        dlg = wx.ProgressDialog('Deleting Bind Files', '',
            maximum = totalfiles, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)

        # try all 15k+ of the files
        progress = 0
        removed = 0
        for file in bindfiles['files']:
            if not file.Path.is_relative_to(bindpath):
                wx.LogWarning(f"Bindfile {file.Path} not in {bindpath}, skipping deletion!")
            elif file.Path.is_file():
                file.Path.unlink()
                removed = removed + 1

            dlg.Update(progress, str(file.Path))
            progress = progress + 1

        # try the directories
        for bdir in bindfiles['dirs']:
            dirpath = Path(self.BindsDir() / bdir)
            if dirpath.is_dir():
                # try / except because if it's not empty it'll barf.
                try:
                    dirpath.rmdir()
                    # not incrementing "removed" here because we just want to count
                    # files, so we can match "wrote X files" with "deleted X files"
                    pass
                except Exception:
                    pass

            dlg.Update(progress, bdir)
            progress = progress + 1

        # remove the bindsdir itself, if empty
        bindsdir = Path(self.BindsDir())
        try:
            bindsdir.rmdir()
        except Exception:
            pass

        # clear out our state
        self.BindFiles = {}

        return removed

class WriteDoneDialog(wx.Dialog):
    def __init__(self, parent, msg = ''):
        wx.Dialog.__init__(self, parent, title = "Bindfiles Written")

        sizer = wx.BoxSizer(wx.VERTICAL)

        msg = msg + (
            "\n\n"
            "If you are updating existing installed BindControl binds,\n"
            f"you can press \"{wx.ConfigBase.Get().Read('ResetKey')}\" in-game to load your new binds.\n"
            "\n"
            "If this is a new set of keybinds, log on to the character\n"
            "you made them for and type into the chat window:"
        )
        sizer.Add(
            wx.StaticText(self, label = msg, style = wx.ALIGN_CENTER),
            0, wx.EXPAND|wx.ALL, 10
        )

        ### helpful copyable /blf text
        blfSizer = wx.BoxSizer(wx.HORIZONTAL)
        textCtrl = wx.TextCtrl(self, id = wx.ID_ANY,
                       style = wx.TE_READONLY|wx.TE_CENTER,
                       value = "/bindloadfile " + str(parent.GameBindsDir() / "reset.txt")
        )
        textCtrl.SetFont(
            wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = 'Courier')
        )
        # https://wxpython.org/Phoenix/docs/html/wx.Control.html#wx.Control.GetSizeFromTextSize
        textCtrl.SetInitialSize(
            textCtrl.GetSizeFromTextSize(
                textCtrl.GetTextExtent(
                    textCtrl.GetValue()
                )
            )
        )
        blfSizer.Add(textCtrl, 1, wx.EXPAND)
        copyButton = wx.BitmapButton(self, bitmap = GetIcon('UI/copy'))
        setattr(copyButton, 'textctrl', textCtrl)
        blfSizer.Add(copyButton, 0)
        copyButton.Bind(wx.EVT_BUTTON, self.doTextCopy)
        sizer.Add(blfSizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        ### "Files Written" list
        fileslist = wx.TextCtrl(self, id = wx.ID_ANY, size=(-1,150),
                                value = "reset.txt\n", style = wx.TE_READONLY|wx.TE_MULTILINE)
        for filename in sorted(parent.BindFiles.keys()):
            if filename == "reset.txt": continue
            bindfile = parent.BindFiles[filename]

            displaypath = bindfile.Path.relative_to(parent.BindsDir())

            fileslist.AppendText(f"{displaypath}\n")

        fileslist.SetInsertionPoint(0)

        sizer.Add(wx.StaticText(self, -1, label = "Files written:"), 0, wx.TOP|wx.RIGHT|wx.LEFT, 10)
        sizer.Add(fileslist, 0, wx.ALL|wx.EXPAND, 10)

        sizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizerAndFit(sizer)

    def doTextCopy(self, evt):
        dataObj = wx.TextDataObject(evt.EventObject.textctrl.GetValue())
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Couldn't open the clipboard for copying")

class DeleteDoneDialog(wx.Dialog):
    def __init__(self, parent, removed = 0):
        wx.Dialog.__init__(self, parent, title = "Bindfiles Deleted")

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(
            wx.StaticText(self, label = (
                    f"Deleted {removed} bind files and removed empty directories."
                    "\n\n"
                    "If you had previously loaded this set of binds with a character,"
                    "\n"
                    "you will likely experience bad results until you log into that character and type:"
                ), style = wx.ALIGN_CENTER),
            1, wx.EXPAND|wx.ALL, 10
        )
        textCtrl = wx.TextCtrl(self, id = wx.ID_ANY,
                       style = wx.TE_READONLY|wx.TE_CENTER,
                       value = "/keybind_reset",
        )
        textCtrl.SetFont(
            wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = 'Courier')
        )
        sizer.Add(textCtrl, 0, wx.EXPAND|wx.ALL, 10)

        sizer.Add(
            wx.StaticText(self, label = f"Alternatively, you can Write Binds again at this point for a fresh set of bindfiles.", style = wx.ALIGN_CENTER),
            1, wx.EXPAND|wx.ALL, 10
        )
        sizer.Add( self.CreateButtonSizer(wx.OK), 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizerAndFit(sizer)
