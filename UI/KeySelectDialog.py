import platform
import re
import string
from typing import Dict, List

import wx
import wx.html
import wx.lib.stattext as ST
import wx.lib.newevent

import UI
from UI.ErrorControls import ErrorControlMixin
from bcController import bcController

KeyChanged, EVT_KEY_CHANGED = wx.lib.newevent.NewEvent()
# Platform-specific keycodes for telling left from right
modRawKeyCodes = {}
if platform.system() == 'Windows':
    modRawKeyCodes = {
            160: 'LSHIFT', 161: 'RSHIFT',
            162: 'LCTRL' , 163: 'RCTRL' ,
            164: 'LAlT'  , 165: 'RALT'  ,
    }
elif platform.system() == 'Linux':
    modRawKeyCodes = {
            65505: 'LSHIFT', 65506: 'RSHIFT',
            65507: 'LCTRL' , 65508: 'RCTRL' ,
            65513: 'LALT'  , 65514: 'RALT'  ,
    }
elif platform.system() == 'Darwin':
    modRawKeyCodes = {
            56: 'LSHIFT', 60: 'RSHIFT',
            59: 'LCTRL' , 62: 'RCTRL' ,
            58: 'LALT'  , 61: 'RALT'  ,
    }

class KeySelectDialog(wx.Dialog):
    def __init__(self, button):

        if button.CtlLabel:
            self.Desc    = button.CtlLabel.GetLabel()
        else:
            self.Desc    = UI.Labels.get(button.CtlName, 'this button')
        self.Button  = button
        self.Binding = button.Key

        self.modKeys: List[str] = [] # gets set every ShowModal() call

        wx.Dialog.__init__(self, button.Parent, -1, self.Desc, style = wx.WANTS_CHARS|wx.DEFAULT_DIALOG_STYLE)

        self.controller = bcController()
        self.controller.SetCapture(self)

        # Mystery panel must be in here in order to get key events
        self.mysteryPanel = wx.Panel(self, -1)

        if not self.Desc:
            raise Exception("Tried to make a KeySelectDialog for something with no desc")

        desc = f"Press the key you want bound to {self.Desc}\n(Right-click a key button to clear it.)"

        # is this ugly?
        self.ModSlot = set()
        self.KeySlot = None
        self.PressedKeys = set()
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

        if(modRawKeyCodes):
            self.SeparateLRChooser = wx.CheckBox( self, -1, "Bind left/right mod keys separately")
            self.SeparateLRChooser.SetToolTip("This allows you to bind specifically left or right side mod keys for this bind.  This will not change the global preference.")
            sizer.Add( self.SeparateLRChooser, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
            self.SeparateLRChooser.SetValue( wx.ConfigBase.Get().ReadBool('UseSplitModKeys') )

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        # clearly I'm thinking of this the wrong way.
        self.SeparateLRChooser.Bind(wx.EVT_KEY_UP    , self.handleKeyUp )
        self.SeparateLRChooser.Bind(wx.EVT_CHAR_HOOK , self.handleCharHook )
        for i in (self.mysteryPanel, self.kbDesc, self.kbBind, self.kbErr, self):
            i.Bind(wx.EVT_KEY_UP          , self.handleKeyUp )
            i.Bind(wx.EVT_CHAR_HOOK       , self.handleCharHook )

            i.Bind(wx.EVT_JOYSTICK_EVENTS , self.handleJS )

            i.Bind(wx.EVT_LEFT_DOWN       , self.handleMouse )
            i.Bind(wx.EVT_MIDDLE_DOWN     , self.handleMouse )
            i.Bind(wx.EVT_RIGHT_DOWN      , self.handleMouse )
            i.Bind(wx.EVT_LEFT_DCLICK     , self.handleMouse )
            i.Bind(wx.EVT_RIGHT_DCLICK    , self.handleMouse )
            i.Bind(wx.EVT_MOUSE_AUX1_DOWN , self.handleMouse )
            i.Bind(wx.EVT_MOUSE_AUX2_DOWN , self.handleMouse )
            i.Bind(wx.EVT_MOUSEWHEEL      , self.handleMouse )

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

    def handleJS(self, event):
        # knock wood, this seems to be working fairly well now.
        if event.ButtonDown() or event.IsMove() or event.IsZMove():
            # iterate joystick buttons and add those that are pressed
            for button in range(0, self.controller.GetNumberButtons()):
                button_keyname = "JOY" + str(button+1)
                if self.controller.GetButtonState(button):
                    self.PressedKeys.add(self.Keymap[button_keyname])
                else:
                    self.PressedKeys.discard(self.Keymap[button_keyname])

            self.controller.SetCurrentAxisPercents()
            # don't let wee jiggles at the center trigger this.
            # this is "no axis is > 50% in some direction" and "POV is centered"
            if self.controller.StickIsNearCenter() and self.controller.GetPOVPosition() > 60000:
                return

            # iterate axes and discard() all;  then add the current one
            # this means they have to hold the axis while clicking "OK" which
            # is less than great but we can't detect intent in software.
            for axis_code in self.controller.GetAllAxisCodes():
                self.PressedKeys.discard(self.Keymap[axis_code])

            current_axis = self.controller.GetCurrentAxis()
            if current_axis:
                self.PressedKeys.add(self.Keymap[current_axis])

        else:
            # Unknown joystick event.  These fire quite a bit.
            return

        self.buildBind()

    def handleCharHook(self, event):
        # Key down
        SeparateLR = self.SeparateLRChooser.Value

        # close the dialog on ESCAPE
        if (isinstance(event, wx.KeyEvent)):
            if event.GetKeyCode() == wx.WXK_ESCAPE:
                self.EndModal(wx.CANCEL)
                return

        rkc = event.GetRawKeyCode()
        if SeparateLR and rkc in modRawKeyCodes:
            self.PressedKeys.add(modRawKeyCodes[rkc])
        else:
            self.clearMouseKeys()
            self.PressedKeys.add(self.Keymap[event.GetKeyCode()])

        self.buildBind()

    def handleKeyUp(self, event):
        # Key-up:  clear keys that were released
        SeparateLR = self.SeparateLRChooser.Value
        rkc = event.GetRawKeyCode()

        if SeparateLR and rkc in modRawKeyCodes:
            self.PressedKeys.discard(modRawKeyCodes[rkc])
        else:
            self.PressedKeys.discard(self.Keymap[event.GetKeyCode()])

        self.buildBind()

    def handleMouse(self, event):
        self.clearMouseKeys()
        if event.GetEventType() == wx.wxEVT_MOUSEWHEEL:
            self.PressedKeys.add("MOUSEWHEEL")
        elif (event.LeftIsDown() and event.RightIsDown()):
            self.PressedKeys.add("MOUSECHORD")
        elif (event.ButtonDClick()):
            self.PressedKeys.add("DCLICK" + str(event.GetButton()))
        else:
            self.PressedKeys.add("BUTTON" + str(event.GetButton()))

        self.buildBind()

    def clearMouseKeys(self):
        pressedkeys = list(self.PressedKeys)
        for key in pressedkeys:
            if re.match("DCLICK", key) or re.match("BUTTON", key):
                self.PressedKeys.discard(key)
        self.PressedKeys.discard("MOUSEWHEEL")
        self.PressedKeys.discard("MOUSECHORD")


    def buildBind(self):
        SeparateLR = self.SeparateLRChooser.Value

        # If we're completely off the keyboard/etc, clear our current state,
        # but return so we don't update the binding to nothing
        if not self.PressedKeys:
            self.ModSlot = set()
            self.KeySlot = None
            return

        for key in self.PressedKeys:
            if key in self.modKeys:
                self.ModSlot.add(key)
            else:
                self.KeySlot = key

        # If we switched SeparateLR midstream, we might get LSHIFT and SHIFT both in there.
        # Clear up that situation
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
            conflicts = self.Button.CheckConflicts(self.Binding)
            if conflicts:
                conflictStrings = []
                for conflict in conflicts:
                    conflictStrings.append(f'Conflict with "{conflict["ctrl"]}" on {conflict["page"]} page.')
                self.kbErr.SetForegroundColour(wx.RED)
                self.kbErr.SetLabel("\n".join(conflictStrings))
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
                wx.WXK_SNAPSHOT : 'SYSRQ', # TODO - this is for Windows;  it only fires a KeyUp event.  Bug in wx?
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
                wx.WXK_NUMLOCK : 'NUMLOCK',
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
                ord('.') : 'PERIOD',
                ord('<') : 'COMMA',
                ord('>') : 'PERIOD',
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
class bcKeyButton(ErrorControlMixin, wx.Button):

    def __init__(self, parent, id, init = {}):
        self.CtlName  : str                                     = init.get('CtlName', None)
        self.CtlLabel : ST.GenStaticText | wx.StaticText | None = init.get('CtlLabel', None)
        self.Key      : str                                     = init.get('Key', '')
        self.Page                                               = parent
        self.AlwaysShorten : bool                               = init.get('AlwaysShorten', False)
        self.Errors   : dict                                    = {}

        # This might be overloading "AlwaysShorten", but:
        style = wx.BU_EXACTFIT if self.AlwaysShorten else 0

        wx.Button.__init__(self, parent, id, style = style)

        self.SetLabel(self.Key)

        self.Bind(wx.EVT_BUTTON, self.KeySelectEventHandler)
        self.Bind(wx.EVT_RIGHT_DOWN, self.ClearButton)
        self.Bind(EVT_KEY_CHANGED, self.onKeyChanged)

    def onKeyChanged(self, _):
        wx.App.Get().Profile.CheckAllConflicts()

    def ClearButton(self, _):
        self.SetLabel("")
        self.Key = ""
        wx.PostEvent(self, KeyChanged())

    def MakeFileKeyBind(self, contents):
        return KeyBind(self.Key, self.CtlLabel, self.Page, contents)

    def SetLabel(self, label):
        # if we have a long label or AlwaysShorten, smallify, and abbreviate if we have a mod key
        if re.search(r'\+\w\w\w\w\w', label) or len(label) > 12 or self.AlwaysShorten:
            if self.AlwaysShorten:
                label = re.sub(r'SHIFT\+', 'S+', label)
                label = re.sub(r'CTRL\+', 'C+', label)
                label = re.sub(r'ALT\+', 'A+', label)
            else:
                label = re.sub(r'SHIFT\+', 'Sh+', label)
                label = re.sub(r'CTRL\+', 'Ctl+', label)
                label = re.sub(r'ALT\+', 'Alt+', label)
            label = re.sub(r'DOUBLECLICK', 'DCLICK', label)
            label = re.sub(r'Trigger', 'Trig', label)
            label = re.sub(r'LeftBumper', 'LBump', label)
            label = re.sub(r'RightBumper', 'RBump', label)
            label = f"<small>{label}</small>"
        self.SetLabelMarkup(label)

    def CheckConflicts(self, newbinding = None):
        Profile = wx.App.Get().Profile
        if Profile:
            conflicts = Profile.CheckConflict(newbinding or self.Key, self.CtlName)
            if conflicts:
                conflictStrings = []
                for conflict in conflicts:
                    conflictStrings.append(f'This key conflicts with \"{conflict["ctrl"]}\" on the \"{conflict["page"]}\" tab.')
                self.AddError('conflict', '\n'.join(conflictStrings))
            else:
                self.RemoveError('conflict')
            return conflicts

    def KeySelectEventHandler(self, evt):
        button = evt.EventObject
        Profile = wx.App.Get().Profile

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
                    Profile.SetModified()

            Profile.CheckAllConflicts()
