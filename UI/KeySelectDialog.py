import re
import wx
import wx.html
import string
import UI
import wx.lib.newevent
from bcController import bcController

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

modKeys = ['SHIFT', 'LSHIFT', 'RSHIFT', 'ALT', 'RALT', 'LALT', 'CTRL', 'LCTRL', 'RCTRL',
        # TODO - set up a place in Preferences to pick which controller thingies are mod keys, but for now:
        'LTrigger', 'RTrigger', 'LeftBumper', 'RightBumper', 'JOY9', 'JOY10',
]

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

        self.controller = bcController()
        self.controller.SetCapture(self)

        # Mystery panel must be in here in order to get key events
        _ = wx.Panel(self, -1)

        if not self.Desc:
            raise Exception("Tried to make a KeySelectDialog for something with no desc")

        desc = f"Press the key you want bound to {self.Desc}:"

        # is this ugly?
        self.ModSlot = None
        self.KeySlot = None
        self.SetKeymap();

        sizer = wx.BoxSizer(wx.VERTICAL);

        self.kbDesc = wx.StaticText( self, -1, desc, style = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        self.kbBind = wx.html.HtmlWindow( self, -1, size=(360,60), style=wx.html.HW_SCROLLBAR_NEVER)
        self.kbBind.SetHTMLBackgroundColour(self.GetBackgroundColour())
        self.kbErr  = wx.StaticText( self, -1, " ", style = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)

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

            i.Bind(wx.EVT_JOYSTICK_EVENTS , self.handleBind )

        buttonSizer = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
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
        pressed_mods = []
        pressed_keys = []

        if (isinstance(event, wx.KeyEvent)):
            if event.GetKeyCode() == wx.WXK_ESCAPE:
                self.EndModal(wx.CANCEL)

        elif (isinstance(event, wx.JoystickEvent)):
            if event.ButtonDown():
                # Carry on, we'll handle these below
                pass
            elif event.IsMove() or event.IsZMove():
                # don't let wee jiggles at the center trigger SetCurrentAxis()
                self.controller.SetCurrentAxisPercents()
                # this is "no axis is > 50% in some direction" and "POV is centered"
                if self.controller.StickIsNearCenter() and self.controller.GetPOVPosition() > 60000:
                    return
            else:
                # Unknown joystick event.  These fire quite a bit.
                return

        elif (event.ButtonDClick()):
            pressed_keys.append("DCLICK" + str(event.GetButton()))
        else:
            pressed_keys.append("BUTTON" + str(event.GetButton()))

        # iterate all possible values, and see if they're currently held down.
        # this applies to keystrokes and joystick axes.  js buttons and mouse
        # clicks have already been added.  This might not be optimal.
        for possible_key in self.Keymap:
            # actual keys are ints in the list
            if (isinstance(possible_key, int) and wx.GetKeyState(possible_key)
                    or
                self.controller.IsOk() and (possible_key == self.controller.GetCurrentAxis())):

                pressed_keys.append(self.Keymap[possible_key])

        # iterate joystick buttons and add those that are pressed
        if self.controller.IsOk():
            print("Looking at buttons")
            for button in range(0, self.controller.GetNumberButtons()):
                if self.controller.GetButtonState(button):
                    button_keyname = "JOY" + str(button+1)
                    pressed_keys.append(self.Keymap[button_keyname])

        # If we're completely off the keyboard/etc, clear our current state,
        # but return so we don't update the binding to nothing
        if not pressed_keys:
            self.KeySlot = self.ModSlot = ''
            return

        # massage keyboard mods if "separate L/R" is active
        if self.SeparateLRChooser.Value and isinstance(event, wx.KeyEvent):
            self.FixLRModKeys(event, pressed_keys)

        for key in pressed_keys:
            if key in modKeys:
                pressed_keys.remove(key)
                pressed_mods.append(key)

        if pressed_keys:
            if pressed_mods:
                self.ModSlot = pressed_mods[0]
            else:
                self.ModSlot = ''
            self.KeySlot = pressed_keys[0]
        else:
            # no pressed keys, so put the first mod in as the KeySlot
            self.ModSlot = ''
            if not pressed_mods:
                self.KeySlot = ''
            else:
                self.KeySlot = pressed_mods[0]

        if self.ModSlot or self.KeySlot:
            self.Binding = "+".join([ key for key in [self.ModSlot, self.KeySlot] if key])

        self.ShowBind()

        self.CheckConflicts()

        self.Layout()

    def CheckConflicts(self):
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
                self.kbBind.SetHTMLBackgroundColour(wx.WHITE)

    def FixLRModKeys(self, event, pressed_keys):
        for key in pressed_keys:
            new_mod = None
            rawFlags = event.GetRawKeyFlags()
            if key == "SHIFT":
                if wx.Platform == '__WXMAC__':
                    new_mod = "LSHIFT" if (rawFlags & modKeyFlags['LSHIFT']) else "RSHIFT"
                else:
                    new_mod = "RSHIFT" if (rawFlags & modKeyFlags['RSHIFT']) else "LSHIFT"

            if key == "CTRL":
                if wx.Platform == '__WXMAC__':
                    new_mod = "LCTRL" if (rawFlags & modKeyFlags['LCTRL']) else "RCTRL"
                elif wx.Platform == '__WXGTK__':
                    new_mod = "LCTRL" if (rawFlags & modKeyFlags['LCTRL']) else "RCTRL"
                else:
                    new_mod = "RCTRL" if (rawFlags & modKeyFlags['RCTRL']) else "LCTRL"

            if key == "ALT":
                if wx.Platform == '__WXMAC__':
                    new_mod = "LALT" if (rawFlags & modKeyFlags['LALT']) else "RALT"
                else:
                    new_mod = "RALT" if (rawFlags & modKeyFlags['RALT']) else "LALT"

            if new_mod:
                pressed_keys[pressed_keys.index(key)] = new_mod

    # This keymap code was initially adapted from PADRE < http://padre.perlide.org/ >.
    def SetKeymap(self):
        # key choice list
        self.Keymap = {
                wx.WXK_RETURN : 'ENTER',
                wx.WXK_BACK : 'BACKSPACE',
                wx.WXK_TAB : 'TAB',
                wx.WXK_SHIFT: 'SHIFT',
                wx.WXK_ALT: 'ALT',
                wx.WXK_CONTROL: 'CTRL', # TODO - wx.WXK_RAW_CONTROL for Mac, instead?
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
                'JOY1'  : 'JOY1',
                'JOY2'  : 'JOY2',
                'JOY3'  : 'JOY3',
                'JOY4'  : 'JOY4',
                'JOY5'  : 'LeftBumper',
                'JOY6'  : 'RightBumper',
                'JOY7'  : 'JOY7',
                'JOY8'  : 'JOY8',
                'JOY9'  : 'JOY9',
                'JOY10' : 'JOY10',
                'JOY11' : 'JOY11',
                'JOY12' : 'JOY12',
                'JOY13' : 'JOY13',
                'JOY14' : 'JOY14',
                'JOY15' : 'JOY15',
                'JOY16' : 'JOY16',
                'JOY17' : 'JOY17',
                'JOY18' : 'JOY18',
                'JOY19' : 'JOY19',
                'JOY20' : 'JOY20',
                'JOY21' : 'JOY21',
                'JOY22' : 'JOY22',
                'JOY23' : 'JOY23',
                'JOY24' : 'JOY24',
                'JOY25' : 'JOY25',
                "J1_U" : "JOYSTICK1_UP",
                "J1_D" : "JOYSTICK1_DOWN",
                "J1_L" : "JOYSTICK1_LEFT",
                "J1_R" : "JOYSTICK1_RIGHT",
                # Do these actually exist in the wild?
                #"J2_U" : "JOYSTICK2_UP",
                #"J2_D" : "JOYSTICK2_DOWN",
                "J2_L" : "RTrigger",
                "J2_R" : "LTrigger",
                "J3_U" : "JOYSTICK3_UP",
                "J3_D" : "JOYSTICK3_DOWN",
                "J3_L" : "JOYSTICK3_LEFT",
                "J3_R" : "JOYSTICK3_RIGHT",
                "JP_U" : "JOYPAD_UP",
                "JP_D" : "JOYPAD_DOWN",
                "JP_L" : "JOYPAD_LEFT",
                "JP_R" : "JOYPAD_RIGHT",
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
            keyLabel = re.sub(r'SHIFT\+', 'S+', keyLabel)
            keyLabel = re.sub(r'CTRL\+', 'C+', keyLabel)
            keyLabel = re.sub(r'ALT\+', 'A+', keyLabel)
            keyLabel = re.sub(r'DOUBLECLICK', 'DCLICK', keyLabel)
            keyLabel = re.sub(r'Trigger', 'Trig', keyLabel)
            keyLabel = re.sub(r'LeftBumper', 'LBump', keyLabel)
            keyLabel = re.sub(r'RightBumper', 'RBump', keyLabel)
            keyLabel = f"<small>{keyLabel}</small>"
        self.SetLabelMarkup(keyLabel)
