import re
import wx
import wx.html
import string
import UI
import wx.lib.newevent
KeyChanged, EVT_KEY_CHANGED = wx.lib.newevent.NewEvent()

# Platform-specific keyevent flags for telling left from right
modKeyFlags = {}
if wx.Platform == '__WXMSW__':
    modKeyFlags = {
        'RSHIFT': 0x40000,
        'RCTRL' : 0x1000000,
        'RALT'  : 0x1000000,
    }
elif wx.Platform == '__WXGTK__':
    modKeyFlags = {
        'RSHIFT': 0x08,
        'LCTRL' : 0x04,
        'RALT'  : 0x08,
    }
elif wx.Platform == '__WXMAC__':
    modKeyFlags = {
        'LSHIFT': 0x02,
        'LCTRL' : 0x2000,
        'LALT'  : 0x20,
    }

def KeySelectEventHandler(evt):
    button = evt.EventObject

    with KeySelectDialog(button) as dlg:
        newKey = ''
        if(dlg.ShowModal() == wx.ID_OK): newKey = dlg.Binding

        # re-label the button / set its state
        if newKey:
            button.Key = newKey
            button.SetLabel(newKey)
            wx.PostEvent(button, KeyChanged())

class KeySelectDialog(wx.Dialog):
    def __init__(self, button):

        self.Desc    = UI.Labels[button.CtlName]
        self.Button  = button
        self.Binding = button.Key

        wx.Dialog.__init__(self, button.Parent, -1, self.Desc, style = wx.WANTS_CHARS|wx.DEFAULT_DIALOG_STYLE)

        # Mystery panel must be in here in order to get key events
        _ = wx.Panel(self, -1)

        if not self.Desc:
            raise Exception("Tried to make a KeySelectDialog for something with no desc")

        desc = f"Press the key you want bound to {self.Desc}:"

        # is this ugly?
        self.ModSlot = set()
        self.KeySlot = None
        self.SetKeymap();

        sizer = wx.BoxSizer(wx.VERTICAL);

        self.kbDesc = wx.StaticText     ( self, -1, desc,          style = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        self.kbBind = wx.html.HtmlWindow( self, -1, size=(360,60), style=wx.html.HW_SCROLLBAR_NEVER)
        self.kbBind.SetHTMLBackgroundColour( wx.WHITE )
        self.kbErr  = wx.StaticText     ( self, -1, " ",           style = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)

        self.ShowBind()

        sizer.Add( self.kbDesc, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5);
        sizer.Add( self.kbBind, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL);
        sizer.Add( self.kbErr , 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5);
        sizer.AddSpacer(15)

        if(modKeyFlags):
            self.SeparateLRChooser = wx.CheckBox( self, -1, "Bind left/right mod keys separately")
            self.SeparateLRChooser.SetToolTip("This allows you to bind specifically left or right side mod keys for this bind.  This will not change the global preference.")
            sizer.Add( self.SeparateLRChooser, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
            self.SeparateLRChooser.SetValue( wx.ConfigBase.Get().ReadBool('UseSplitModKeys') )

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        # clearly I'm thinking of this the wrong way.
        for i in (self.kbDesc, self.kbBind, self.kbErr, self):
            i.Bind(wx.EVT_CHAR_HOOK       , self.handleBind )

            i.Bind(wx.EVT_LEFT_DOWN       , self.handleBind )
            i.Bind(wx.EVT_MIDDLE_DOWN     , self.handleBind )
            i.Bind(wx.EVT_RIGHT_DOWN      , self.handleBind )
            i.Bind(wx.EVT_LEFT_DCLICK     , self.handleBind )
            i.Bind(wx.EVT_RIGHT_DCLICK    , self.handleBind )
            i.Bind(wx.EVT_MOUSE_AUX1_DOWN , self.handleBind )
            i.Bind(wx.EVT_MOUSE_AUX2_DOWN , self.handleBind )

        buttonSizer = self.CreateButtonSizer(wx.OK|wx.CANCEL|wx.NO_DEFAULT)
        vbox.Add(buttonSizer, 0, wx.ALIGN_CENTER|wx.ALL, 16)

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.SetFocus()

    def ShowBind(self):
        self.kbBind.SetPage('<center><b><font size=+4>' + self.Binding + '</font></b></center>')

    def handleBind(self, event):
        ### Algorithm:
        # two slots, "Mod" and "Key"
        # if normal key, put it in key slot
        # if mod key
        #   if already mod key, AND not the same one, AND still held down
        #       put it in key slot
        #   else
        #       put it in mod slot
        SeparateLR = self.SeparateLRChooser.Value

        # first clear out anything not being held down
        if not event.ControlDown():
            self.ModSlot.discard('CTRL')
            self.ModSlot.discard('LCTRL')
            self.ModSlot.discard('RCTRL')
        if not event.ShiftDown():
            self.ModSlot.discard('SHIFT')
            self.ModSlot.discard('LSHIFT')
            self.ModSlot.discard('RSHIFT')
        if not event.AltDown():
            self.ModSlot.discard('ALT')
            self.ModSlot.discard('LALT')
            self.ModSlot.discard('RALT')

        if (isinstance(event, wx.KeyEvent)):
            code = event.GetKeyCode()
            if code == wx.WXK_ESCAPE:
                self.EndModal(wx.CANCEL)
        elif (event.ButtonDClick()):
            code = "DCLICK" + str(event.GetButton())
        else:
            code = "BUTTON" + str(event.GetButton())

        KeyToBind = self.Keymap.get(code, '')

        if KeyToBind:
            self.KeySlot = KeyToBind
        else:
            if isinstance(event, wx.KeyEvent) and event.HasAnyModifiers():

                if event.ShiftDown():
                    if SeparateLR and modKeyFlags:
                        rawFlags = event.GetRawKeyFlags()
                        if wx.Platform == '__WXMAC__':
                            self.ModSlot.add("LSHIFT") if (rawFlags & modKeyFlags['LSHIFT']) else "RSHIFT"
                        else:
                            self.ModSlot.add("RSHIFT") if (rawFlags & modKeyFlags['RSHIFT']) else "LSHIFT"
                    else:
                        self.ModSlot.add("SHIFT")

                if event.ControlDown():
                    if SeparateLR and modKeyFlags:
                        rawFlags = event.GetRawKeyFlags()
                        if wx.Platform == '__WXMAC__':
                            self.ModSlot.add("LCTRL") if (rawFlags & modKeyFlags['LCTRL']) else "RCTRL"
                        elif wx.Platform == '__WXGTK__':
                            self.ModSlot.add("LCTRL") if (rawFlags & modKeyFlags['LCTRL']) else "RCTRL"
                        else:
                            self.ModSlot.add("RCTRL") if (rawFlags & modKeyFlags['RCTRL']) else "LCTRL"
                    else:
                        self.ModSlot.add("CTRL")

                if event.AltDown():
                    if SeparateLR and modKeyFlags:
                        rawFlags = event.GetRawKeyFlags()
                        if wx.Platform == '__WXMAC__':
                            self.ModSlot.add("LALT") if (rawFlags & modKeyFlags['LALT']) else "RALT"
                        else:
                            self.ModSlot.add("RALT") if (rawFlags & modKeyFlags['RALT']) else "LALT"
                    else:
                        self.ModSlot.add("ALT")

        ModKeys      = "+".join([ key for key in sorted(self.ModSlot, reverse=True) if key])
        self.Binding = "+".join([ key for key in [ModKeys, self.KeySlot] if key])

        self.ShowBind()

        Profile = wx.App.Get().Profile
        if Profile:
            conflicts = Profile.CheckConflict(self.Binding)
            if conflicts:
                conflictString = ''
                for conflict in conflicts:
                    conflictString = conflictString + f'Conflict with "{conflict["ctrl"]}" on {conflict["page"]} page.'
                self.kbErr.SetForegroundColour(wx.RED)
                self.kbErr.SetLabel(conflictString)
                self.kbBind.SetHTMLBackgroundColour((255,200,200))
            else:
                self.kbErr.SetForegroundColour(wx.NullColour)
                self.kbErr.SetLabel(" ")
                self.kbBind.SetHTMLBackgroundColour( wx.WHITE )

        self.Layout()

    # This keymap code was initially adapted from PADRE < http://padre.perlide.org/ >.
    def SetKeymap(self):
        # key choice list
        self.Keymap = {
                wx.WXK_RETURN : 'ENTER',
                wx.WXK_BACK : 'BACKSPACE',
                wx.WXK_TAB : 'TAB',
                wx.WXK_SPACE : 'SPACE',
                wx.WXK_UP : 'UP',
                wx.WXK_DOWN : 'DOWN',
                wx.WXK_LEFT : 'LEFT',
                wx.WXK_RIGHT : 'RIGHT',
                wx.WXK_INSERT : 'INSERT',
                wx.WXK_DELETE : 'DELETE',
                wx.WXK_HOME : 'HOME',
                wx.WXK_END : 'END',
                wx.WXK_CAPITAL : 'CAPITAL',
                wx.WXK_PAGEUP : 'PAGEUP',
                wx.WXK_PAGEDOWN : 'PAGEDOWN',
                wx.WXK_PRINT : 'SYSRQ',
                wx.WXK_SCROLL : 'SCROLL',
                wx.WXK_MENU : 'APPS',
                wx.WXK_PAUSE : 'PAUSE',
                wx.WXK_NUMPAD0 : 'NUMPAD0',
                wx.WXK_NUMPAD1 : 'NUMPAD1',
                wx.WXK_NUMPAD2 : 'NUMPAD2',
                wx.WXK_NUMPAD3 : 'NUMPAD3',
                wx.WXK_NUMPAD4 : 'NUMPAD4',
                wx.WXK_NUMPAD5 : 'NUMPAD5',
                wx.WXK_NUMPAD6 : 'NUMPAD6',
                wx.WXK_NUMPAD7 : 'NUMPAD7',
                wx.WXK_NUMPAD8 : 'NUMPAD8',
                wx.WXK_NUMPAD9 : 'NUMPAD9',
                wx.WXK_NUMPAD_MULTIPLY : 'MULTIPLY',
                wx.WXK_NUMPAD_ADD : 'ADD',
                wx.WXK_NUMPAD_SUBTRACT : 'SUBTRACT',
                wx.WXK_NUMPAD_DECIMAL : 'DECIMAL',
                wx.WXK_NUMPAD_DIVIDE : 'DIVIDE',
                wx.WXK_NUMPAD_ENTER : 'NUMPADENTER',
                wx.WXK_F1 : 'F1',
                wx.WXK_F2 : 'F2',
                wx.WXK_F3 : 'F3',
                wx.WXK_F4 : 'F4',
                wx.WXK_F5 : 'F5',
                wx.WXK_F6 : 'F6',
                wx.WXK_F7 : 'F7',
                wx.WXK_F8 : 'F8',
                wx.WXK_F9 : 'F9',
                wx.WXK_F10 : 'F10',
                wx.WXK_F11 : 'F11',
                wx.WXK_F12 : 'F12',
                wx.WXK_F13 : 'F13',
                wx.WXK_F14 : 'F14',
                wx.WXK_F15 : 'F15',
                wx.WXK_F16 : 'F16',
                wx.WXK_F17 : 'F17',
                wx.WXK_F18 : 'F18',
                wx.WXK_F19 : 'F19',
                wx.WXK_F20 : 'F20',
                wx.WXK_F21 : 'F21',
                wx.WXK_F22 : 'F22',
                wx.WXK_F23 : 'F23',
                wx.WXK_F24 : 'F24',
                ord('`') : 'TILDE',
                ord('-') : '-',
                ord('=') : 'EQUALS',
                ord('[') : '[',
                ord(']') : ']',
                ord("\\") : "\\",
                ord(';') : ';',
                ord("'") : "'",
                ord(',') : 'COMMA',
                ord('.') : '.',
                ord('/') : '/',
                'BUTTON1' : 'LBUTTON',
                'BUTTON2' : 'MBUTTON',
                'BUTTON3' : 'RBUTTON',
                'BUTTON4' : 'BUTTON4',
                'BUTTON5' : 'BUTTON5',
                'BUTTON6' : 'BUTTON6',
                'BUTTON7' : 'BUTTON7',
                'BUTTON8' : 'BUTTON8',
                'DCLICK1' : 'LEFTDOUBLECLICK',
                'DCLICK3' : 'RIGHTDOUBLECLICK',
        }

        # Add alphanumerics
        for alphanum in (list(string.ascii_uppercase) + list(range(10))):
            self.Keymap[ord(str(alphanum))] = str(alphanum)

from BindFile import KeyBind
from Page import Page
class bcKeyButton(wx.Button):

    def __init__(self, parent, id, init = {}):
        wx.Button.__init__(self, parent, id)
        self.CtlName  : str           = init.get('CtlName', None)
        self.CtlLabel : wx.StaticText = init.get('CtlLabel', None)
        self.Key      : str           = init.get('Key', '')
        self.Page     : Page          = parent

        self.SetLabel(self.Key)

        self.Bind(wx.EVT_BUTTON, KeySelectEventHandler)
        self.Bind(wx.EVT_RIGHT_DOWN, self.ClearButton)

    def ClearButton(self, _):
        self.SetLabel("")
        self.Key = ""
        wx.PostEvent(self, KeyChanged())

    def MakeFileKeyBind(self, contents):
        return KeyBind(self.Key, self.CtlLabel, self.Page, contents)

    def SetLabel(self, keyLabel):
        if re.search(r'\+\w\w\w\w\w', keyLabel) or len(keyLabel) > 12:
            # smallify and abbreviate if we have a mod key
            keyLabel = re.sub(r'SHIFT\+', 'Sh+', keyLabel)
            keyLabel = re.sub(r'CTRL\+', 'Ctl+', keyLabel)
            keyLabel = re.sub(r'ALT\+', 'Alt+', keyLabel)
            keyLabel = re.sub(r'DOUBLECLICK', 'DCLICK', keyLabel)
            keyLabel = f"<small>{keyLabel}</small>"
        self.SetLabelMarkup(keyLabel)
