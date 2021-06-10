import wx
import string
import UI
import Utility

# Platform-specific keyevent flags for telling left from right
modKeyFlags = {}
if wx.Platform == '__WXMSW__':
    modKeyFlags = {
        'RSHIFT': 0x40000,
        'RCTRL' : 0x1000000,
        'RALT'  : 0x1000000,
    }
elif wx.Platform == '__WXX11_':
    modKeyFlags = {
        'LSHIFT': 65505, 'RSHIFT': 65506,
        'LCTRL' : 65507, 'RCTRL' : 65508,
        'LALT'  : 65513, 'RALT'  : 65514
    }
elif wx.Platform == '__WXMAC__':
    pass



def KeyPickerEventHandler(evt):
    button = evt.EventObject

    with KeyBindDialog(button.Parent, button.CtlName, button.Label) as dlg:
        newKey = ''
        if(dlg.ShowModal() == wx.ID_OK): newKey = dlg.Binding

        # TODO -- check for conflicts
        # otherThingWithThatBind = checkConflicts(newKey)

        # re-label the button / set its state
        if newKey:
            evt.EventObject.SetLabel(newKey)

class KeyBindDialog(wx.Dialog):
    def __init__(self, parent, desc = '', keybind = 'UNBOUND'):
        wx.Dialog.__init__(self, parent, -1, style = wx.WANTS_CHARS|wx.DEFAULT_DIALOG_STYLE)

        if not desc:
            print("Tried to make a KeyBindDialog for something with no desc")
            return

        desc = f"Press the key you want bound to {UI.Labels.get(desc, desc)}:"

        self.Binding   = ''
        self.ShiftText = ''
        self.CtrlText  = ''
        self.AltText   = ''
        self.SetKeymap();

        sizer = wx.BoxSizer(wx.VERTICAL);

        self.kbDesc = wx.StaticText( self, -1, desc,    style = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.kbBind = wx.StaticText( self, -1, keybind, style = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        self.kbBind.SetLabelMarkup('<b><big>' + keybind + '</big></b>')

        self.SeparateLRChooser = wx.CheckBox( self, -1, "Bind left/right mod keys separately")

        sizer.Add( self.kbDesc, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 15);
        sizer.Add( self.kbBind, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 15);
        sizer.AddSpacer(15)
        sizer.Add( self.SeparateLRChooser, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        # clearly I'm thinking of this the wrong way.
        for i in (self.kbDesc, self.kbBind, self):
            i.Bind(wx.EVT_CHAR_HOOK       , self.handleBind )

            i.Bind(wx.EVT_LEFT_DOWN       , self.handleBind )
            i.Bind(wx.EVT_MIDDLE_DOWN     , self.handleBind )
            i.Bind(wx.EVT_RIGHT_DOWN      , self.handleBind )
            i.Bind(wx.EVT_MOUSE_AUX1_DOWN , self.handleBind )
            i.Bind(wx.EVT_MOUSE_AUX2_DOWN , self.handleBind )

        buttonSizer = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        vbox.Add(buttonSizer, 0, wx.ALIGN_CENTER|wx.ALL, 16)

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.SetFocus()

    def ShowWindow(self, *args):
        # self.Populate(args);

        result = self.ShowModal()

        if (result == wx.OK or result == wx.APPLY): return self.Binding

    def Populate(self, parent, id, current):
        self.kbDesc.SetLabel(f"Press the Key Combo you'd like to use for {UI.Labels[id]}");
        self.kbBind.SetLabel(current);
        self.Fit();
        self.CentreOnParent();


    def handleBind(self, event):

        evtType = event.GetEventType();

        KeyToBind = ''

        SeparateLR = self.SeparateLRChooser.Value

        if (isinstance(event, wx.KeyEvent)):
            code = event.GetKeyCode()

            KeyToBind = self.Keymap.get(code, '')
        else:
            button = event.GetButton()
            KeyToBind = [
                '', # 'button zero' placeholder
                'LBUTTON',
                'MBUTTON',
                'RBUTTON',
                'BUTTON4',
                'BUTTON5',
                'BUTTON6',
                'BUTTON7',
                'BUTTON8',
            ][button]

        # check for each modifier key
        if (event.ShiftDown()) :
            if SeparateLR and modKeyFlags:
                if isinstance(event, wx.KeyEvent):
                    rawFlags = event.GetRawKeyFlags()
                    if not rawFlags: print("NO RAWFLAGS")
                    print(bin(rawFlags))
                    self.ShiftText = "RSHIFT+" if (rawFlags & modKeyFlags['RSHIFT']) else "LSHIFT+"
            else:
                self.ShiftText = "SHIFT+"
        else:
            self.ShiftText = ''

        if (event.CmdDown())   :
            if SeparateLR and modKeyFlags:
                if isinstance(event, wx.KeyEvent):
                    rawFlags = event.GetRawKeyFlags()
                    print(hex(rawFlags))
                    print(bin(rawFlags))
                    self.CtrlText = "RCTRL+" if (rawFlags & modKeyFlags['RCTRL']) else "LCTRL+"
            else:
                self.CtrlText = "CTRL+"
        else:
            self.CtrlText = ''

        # TODO - Alt goes missing if you mash several things while the dialog is open
        if (event.AltDown())   :
            if SeparateLR and modKeyFlags:
                if isinstance(event, wx.KeyEvent):
                    rawFlags = event.GetRawKeyFlags()
                    print(hex(rawFlags))
                    print(bin(rawFlags))
                    self.AltText = "RALT+" if (rawFlags & modKeyFlags['RALT']) else "LALT+"
            else:
                self.AltText = "ALT+"
        else:
            self.AltText = ''

        self.Binding = self.CtrlText + self.AltText + self.ShiftText + str(KeyToBind)
        print(self.Binding)

        self.kbBind.SetLabelMarkup('<b><big>' + self.Binding + '</big></b>')
        self.Layout()

    # This keymap code was initially adapted from PADRE < http://padre.perlide.org/ >.
    def SetKeymap(self):
        # key choice list
        self.Keymap = {
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
        }

        # Add alphanumerics
        for alphanum in (list(string.ascii_uppercase) + list(range(10))):
                self.Keymap[ord(str(alphanum))] = alphanum


