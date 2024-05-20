import platform
import re
import string
from typing import Dict, List

import wx
import wx.html
import wx.lib.stattext as ST
import wx.lib.newevent

import UI
from bcController import bcController

KeyChanged, EVT_KEY_CHANGED = wx.lib.newevent.NewEvent()

# Platform-specific keyevent flags for telling left from right
modKeyFlags = {}
if platform.system() == 'Windows':
    modKeyFlags = {
        'RSHIFT': 0x40000,
        'RCTRL' : 0x1000000,
        'RALT'  : 0x1000000,
    }
elif platform.system() == 'Linux':
    modKeyFlags = {
        'RSHIFT': 0x08,
        'LCTRL' : 0x04,
        'RALT'  : 0x08,
    }
elif platform.system() == 'Darwin':
    modKeyFlags = {
        'LSHIFT': 0x02,
        'LCTRL' : 0x2000,
        'LALT'  : 0x20,
    }


class KeySelectDialog(wx.Dialog):
    def __init__(self, button):

        self.Desc    = UI.Labels[button.CtlName]
        self.Button  = button
        self.Binding = button.Key

        self.modKeys: List[str] = [] # gets set every ShowModal() call

        wx.Dialog.__init__(self, button.Parent, -1, self.Desc, style = wx.WANTS_CHARS|wx.DEFAULT_DIALOG_STYLE)

        self.controller = bcController()
        self.controller.SetCapture(self)

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

            i.Bind(wx.EVT_JOYSTICK_EVENTS , self.handleBind )

        buttonSizer = self.CreateButtonSizer(wx.OK|wx.CANCEL|wx.NO_DEFAULT)
        vbox.Add(buttonSizer, 0, wx.ALIGN_CENTER|wx.ALL, 16)

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.SetFocus()

    def ShowModal(self):
        # re-set-up ModKeys every time we show the dialog in case prefs changed.
        config = wx.ConfigBase.Get()
        self.modKeys = ['SHIFT', 'LSHIFT', 'RSHIFT', 'ALT', 'RALT', 'LALT', 'CTRL', 'LCTRL', 'RCTRL', ]
        for picker in ['ControllerMod1', 'ControllerMod2', 'ExtraMod1', 'ExtraMod2', 'ExtraMod3', 'ExtraMod4']:
            modkey = config.Read(picker)
            if modkey:
                self.modKeys.append(modkey)

        return super().ShowModal()


    def ShowBind(self):
        self.kbBind.SetPage('<center><b><font size=+4>' + self.Binding + '</font></b></center>')

    def handleBind(self, event):
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
        pressed_keys = set()

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
            pressed_keys.add("DCLICK" + str(event.GetButton()))
        else:
            pressed_keys.add("BUTTON" + str(event.GetButton()))

        # iterate all possible values, and see if they're currently held down.
        # this applies to keystrokes and joystick axes.  js buttons and mouse
        # clicks have already been added.  This might not be optimal.
        for possible_key in self.Keymap:
            if (
                    (
                        # actual keys are ints in the list
                        isinstance(possible_key, int)
                            and
                        (
                            (isinstance(event, wx.KeyEvent) and event.GetKeyCode() == possible_key)
                        )
                    )
                        or
                    self.controller.IsOk() and (possible_key == self.controller.GetCurrentAxis())
                ):
                pressed_keys.add(self.Keymap[possible_key])

        # iterate joystick buttons and add those that are pressed
        if self.controller.IsOk():
            for button in range(0, self.controller.GetNumberButtons()):
                if self.controller.GetButtonState(button):
                    button_keyname = "JOY" + str(button+1)
                    pressed_keys.add(self.Keymap[button_keyname])

        # If we're completely off the keyboard/etc, clear our current state,
        # but return so we don't update the binding to nothing
        if not pressed_keys:
            self.ModSlot = set()
            self.KeySlot = None
            return

        if isinstance(event, wx.KeyEvent) and event.HasAnyModifiers():
            if event.ShiftDown():
                if SeparateLR and modKeyFlags:
                    rawFlags = event.GetRawKeyFlags()
                    if platform.system() == 'Darwin':
                        pressed_keys.add(("LSHIFT") if (rawFlags & modKeyFlags['LSHIFT']) else "RSHIFT")
                    else:
                        pressed_keys.add(("RSHIFT") if (rawFlags & modKeyFlags['RSHIFT']) else "LSHIFT")
                else:
                    pressed_keys.add("SHIFT")

            if event.ControlDown():
                if SeparateLR and modKeyFlags:
                    rawFlags = event.GetRawKeyFlags()
                    if platform.system() == 'Darwin':
                        pressed_keys.add(("LCTRL") if (rawFlags & modKeyFlags['LCTRL']) else "RCTRL")
                    elif platform.system() == 'Linux':
                        pressed_keys.add(("LCTRL") if (rawFlags & modKeyFlags['LCTRL']) else "RCTRL")
                    else:
                        pressed_keys.add(("RCTRL") if (rawFlags & modKeyFlags['RCTRL']) else "LCTRL")
                else:
                    pressed_keys.add("CTRL")

            if event.AltDown():
                if SeparateLR and modKeyFlags:
                    rawFlags = event.GetRawKeyFlags()
                    if platform.system() == 'Darwin':
                        pressed_keys.add(("LALT") if (rawFlags & modKeyFlags['LALT']) else "RALT")
                    else:
                        pressed_keys.add(("RALT") if (rawFlags & modKeyFlags['RALT']) else "LALT")
                else:
                    pressed_keys.add("ALT")

        for key in pressed_keys:
            if key in self.modKeys:
                self.ModSlot.add(key)
            else:
                self.KeySlot = key

        # not clear what the race condition is where we're getting both, say, "SHIFT" and "LSHIFT"
        # into the set, but we'll just manually deconstruct that situation here.
        if ("SHIFT" in self.ModSlot and ("LSHIFT" in self.ModSlot or "RSHIFT" in self.ModSlot)):
            if SeparateLR:
                self.ModSlot.discard("SHIFT")
            else:
                self.ModSlot.discard("LSHIFT")
                self.ModSlot.discard("RSHIFT")

        if ("CTRL" in self.ModSlot and ("LCTRL" in self.ModSlot or "RCTRL" in self.ModSlot)):
            if SeparateLR:
                self.ModSlot.discard("CTRL")
            else:
                self.ModSlot.discard("LCTRL")
                self.ModSlot.discard("RCTRL")

        if ("ALT" in self.ModSlot and ("LALT" in self.ModSlot or "RALT" in self.ModSlot)):
            if SeparateLR:
                self.ModSlot.discard("ALT")
            else:
                self.ModSlot.discard("LALT")
                self.ModSlot.discard("RALT")

        # Finally, build the bind string from what we have left over
        totalModKeys = "+".join([ key for key in sorted(self.ModSlot, reverse=True) if key])
        self.Binding = "+".join([ key for key in [totalModKeys, self.KeySlot] if key])

        self.ShowBind()

        self.CheckConflicts()

        self.Layout()

    def CheckConflicts(self):
        Profile = wx.App.Get().Profile
        if Profile:
            conflicts = Profile.CheckConflict(self.Binding, self.Button.CtlName)
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

    # This keymap code was initially adapted from PADRE < http://padre.perlide.org/ >.
    def SetKeymap(self):
        # key choice list
        self.Keymap: Dict[str|int, str] = {
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
        self.CtlLabel : ST.GenStaticText | wx.StaticText | None = init.get('CtlLabel', None)
        self.Key      : str           = init.get('Key', '')
        self.Page     : Page          = parent

        self.SetLabel(self.Key)

        self.Bind(wx.EVT_BUTTON, self.KeySelectEventHandler)
        self.Bind(wx.EVT_RIGHT_DOWN, self.ClearButton)

    def ClearButton(self, _):
        self.SetLabel("")
        self.Key = ""
        wx.PostEvent(self, KeyChanged())

    def MakeFileKeyBind(self, contents):
        return KeyBind(self.Key, self.CtlLabel, self.Page, contents)

    def SetLabel(self, label):
        if re.search(r'\+\w\w\w\w\w', label) or len(label) > 12:
            # smallify and abbreviate if we have a mod key
            label = re.sub(r'SHIFT\+', 'Sh+', label)
            label = re.sub(r'CTRL\+', 'Ctl+', label)
            label = re.sub(r'ALT\+', 'Alt+', label)
            label = re.sub(r'DOUBLECLICK', 'DCLICK', label)
            label = re.sub(r'Trigger', 'Trig', label)
            label = re.sub(r'LeftBumper', 'LBump', label)
            label = re.sub(r'RightBumper', 'RBump', label)
            label = f"<small>{label}</small>"
        self.SetLabelMarkup(label)

    def KeySelectEventHandler(self, evt):
        button = evt.EventObject

        existingKey = button.Key

        with KeySelectDialog(button) as dlg:
            newKey = ''
            if(dlg.ShowModal() == wx.ID_OK): newKey = dlg.Binding

            # re-label the button / set its state
            if newKey:
                button.Key = newKey
                button.SetLabel(newKey)
                wx.PostEvent(button, KeyChanged())

                if existingKey != newKey:
                    Profile = wx.App.Get().Profile
                    Profile.SetModified()

