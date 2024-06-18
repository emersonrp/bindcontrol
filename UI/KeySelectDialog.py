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

        if button.CtlLabel:
            self.Desc    = button.CtlLabel.GetLabel()
        else:
            self.Desc    = UI.Labels.get(button.CtlName, 'this keybind')
        self.Button  = button
        self.Binding = button.Key

        # prepopulate ModSlot and KeySlot so ShowBind doesn't clear everything
        # on the first event it sees, usually a spurious joystick event
        bindsplit = re.split(r'\+', self.Binding)
        if len(bindsplit) == 2:
            self.ModSlot = bindsplit[0]
            self.KeySlot = bindsplit[1]
        else:
            self.ModSlot = ''
            self.KeySlot = bindsplit[0]

        self.PressedKeys = set()

        self.SetKeymap();

        self.modKeys: List[str] = [] # gets set every ShowModal() call
        self.dualKeys = ['SHIFT','CTRL','ALT'] # keys which might be mod and might be trigger

        wx.Dialog.__init__(self, button.Parent, -1, self.Desc, style = wx.WANTS_CHARS|wx.DEFAULT_DIALOG_STYLE)

        self.controller = bcController()
        self.controller.SetCapture(self)

        # Mystery panel must be in here in order to get key events
        self.mysteryPanel = wx.Panel(self, -1)

        if not self.Desc:
            raise Exception("Tried to make a KeySelectDialog for something with no desc")

        desc = f"Press the key you want bound to {self.Desc}\n(Right-click a key button to clear it.)"

        # is this ugly?
        sizer = wx.BoxSizer(wx.VERTICAL);

        self.kbDesc = wx.StaticText     ( self, -1, desc,          style = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        self.kbBind = wx.html.HtmlWindow( self, -1, size=(450,60), style=wx.html.HW_SCROLLBAR_NEVER)
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
        # we don't want to do this clearing logic with unknown events,
        # hence this tangly "if"
        if (
            (not event.ButtonDown()) and (not event.ButtonUp()) and
            (not event.IsMove())     and (not event.IsZMove())  and
            (not self.controller.GetCurrentAxis())
        ):
            if not self.PressedKeys:
                self.ModSlot = ''
                self.KeySlot = ''

        if event.ButtonDown():
            button_keyname = self.Keymap["JOY" + str(event.GetButtonOrdinal()+1)]
            self.PressedKeys.add(button_keyname)
            if button_keyname in self.modKeys:
                self.ModSlot = button_keyname
            else:
                self.KeySlot = button_keyname

        elif event.ButtonUp():
            button_keyname = self.Keymap["JOY" + str(event.GetButtonOrdinal()+1)]
            self.PressedKeys.discard(button_keyname)

        elif event.IsMove() or event.IsZMove():
            self.controller.SetCurrentAxisPercents()
            # don't let wee jiggles at the center trigger this.
            # this is "no axis is > 50% in some direction" and "POV is centered"
            if self.controller.StickIsNearCenter() and self.controller.GetPOVPosition() > 60000:
                return

            # clear all axes from PressedKeys
            for axis in [
                "JOYSTICK1_UP" , "JOYSTICK1_DOWN" , "JOYSTICK1_LEFT" , "JOYSTICK1_RIGHT" ,
                "RTrigger"     , "LTrigger"       ,
                "JOYSTICK3_UP" , "JOYSTICK3_DOWN" , "JOYSTICK3_LEFT" , "JOYSTICK3_RIGHT" ,
                "JOYPAD_UP"    , "JOYPAD_DOWN"    , "JOYPAD_LEFT"    , "JOYPAD_RIGHT"    ,
            ]:self.PressedKeys.discard(axis)

            current_axis = self.controller.GetCurrentAxis()
            if current_axis:
                payload = self.Keymap[current_axis]
                self.PressedKeys.add(payload)
                if payload in self.modKeys:
                    self.ModSlot = payload
                else:
                    self.KeySlot = payload

        else:
            # Unknown joystick event.  These fire quite a bit.
            return

        self.buildBind()

    def handleCharHook(self, event):
        # Key down

        # close the dialog on ESCAPE
        if (isinstance(event, wx.KeyEvent)):
            if event.GetKeyCode() == wx.WXK_ESCAPE:
                self.EndModal(wx.CANCEL)
                return

        payload = self.GetEventPayload(event)

        if not self.PressedKeys:
            # If we have no pressed keys, ie, we're starting over, clear state and start
            self.KeySlot = payload
            self.ModSlot = ''
        else:
            # we have something held down
            if payload in self.dualKeys:
                # we're handling one of the magical "dual keys"
                if self.ModSlot:
                    # if we have a ModKey already
                    if (self.KeySlot in self.dualKeys and
                        (self.NormalizeDualKeyName(self.KeySlot) != self.NormalizeDualKeyName(payload))
                    ):
                        # If we have a dualkey in the keyslot, and it's not us
                        # (ie, prevent "ALT+ALT"), bump it to the ModSlot and
                        # use us as the KeySlot.
                        #
                        # TODO there's still a weird case where if we are holding down SHIFT
                        # and keep tapping ALT, while LR is true, we get "ALT+LALT"
                        self.ModSlot = self.NormalizeDualKeyName(self.KeySlot)
                        self.KeySlot = payload
                    elif self.ModSlot != self.NormalizeDualKeyName(payload):
                        # if we are not the existing ModSlot, use us as the target key.
                        # ie, we already had "SHIFT" and we hit "CTRL"
                        self.KeySlot = payload
                    # else we have a modslot and we are already it, we're done
                else:
                    # we don't have a modkey, but we have something held down,
                    # so it must be in keyslot.
                    if self.KeySlot in self.dualKeys:
                        # If it's a dualkey in KeySlot, let's bump it to ModSlot
                        # and use this as KeySlot.
                        self.ModSlot = self.NormalizeDualKeyName(self.KeySlot)
                        self.KeySlot = payload
                    else:
                        # it's not a dualkey, so let's be its mod
                        self.ModSlot = payload

            # else this is a "normal" key and we can just DTRT
            else:
                # if we have LSHIFT etc in the keyslot, move it to the modslot.
                # This is probably going to be the path most taken, as people will hit
                # "SHIFT" then "R" or whatever, and we'll initially assign the SHIFT
                # to the KeySlot
                if self.KeySlot in self.modKeys:
                    self.ModSlot = self.NormalizeDualKeyName(self.KeySlot)

                self.KeySlot = payload

        self.PressedKeys.add(payload)

        self.buildBind()

    def GetEventPayload(self, event):
        # fish out the payload name -- upgrade "SHIFT" to "LSHIFT" etc if appropriate
        SeparateLR = self.SeparateLRChooser.Value
        payload    = self.Keymap[event.GetKeyCode()]

        if SeparateLR and modKeyFlags:
            rawFlags = event.GetRawKeyFlags()
            system   = platform.system()
            if payload == "SHIFT":
                if system == 'Darwin':
                    payload = "LSHIFT" if (rawFlags & modKeyFlags['LSHIFT']) else "RSHIFT"
                else:
                    payload = "RSHIFT" if (rawFlags & modKeyFlags['RSHIFT']) else "LSHIFT"

            if payload == "CTRL":
                if system == 'Darwin':
                    payload = "LCTRL" if (rawFlags & modKeyFlags['LCTRL']) else "RCTRL"
                elif system == 'Linux':
                    payload = "LCTRL" if (rawFlags & modKeyFlags['LCTRL']) else "RCTRL"
                else:
                    payload = "RCTRL" if (rawFlags & modKeyFlags['RCTRL']) else "LCTRL"

            if payload == "ALT":
                if system == 'Darwin':
                    payload = "LALT" if (rawFlags & modKeyFlags['LALT']) else "RALT"
                else:
                    payload = "RALT" if (rawFlags & modKeyFlags['RALT']) else "LALT"

        return payload

    def NormalizeDualKeyName(self, name):
        return { 'LSHIFT' : 'SHIFT' , 'RSHIFT' : 'SHIFT' , 'SHIFT' : 'SHIFT' ,
                 'LCTRL'  : 'CTRL'  , 'RCTRL'  : 'CTRL'  , 'CTRL'  : 'CTRL'  ,
                 'LALT'   : 'ALT'   , 'RALT'   : 'ALT'   , 'ALT'   : 'ALT'   ,
        }[name]

    def handleKeyUp(self, event):
        self.PressedKeys.discard(self.GetEventPayload(event))
        self.buildBind()

    def handleMouse(self, event):
        # if nothing's pressed, clear everything
        if not self.PressedKeys:
            self.ModSlot = ''
            self.KeySlot = ''

        # if we have just a modkey, move it over
        if self.KeySlot in self.modKeys:
            self.ModSlot = self.NormalizeDualKeyName(self.KeySlot)

        if event.GetEventType() == wx.wxEVT_MOUSEWHEEL:
            self.KeySlot = "MOUSEWHEEL"
        elif (event.LeftIsDown() and event.RightIsDown()):
            self.KeySlot = "MOUSECHORD"
        elif (event.ButtonDClick()):
            self.KeySlot = "DCLICK" + str(event.GetButton())
        else:
            self.KeySlot = "BUTTON" + str(event.GetButton())

        self.buildBind()

    def buildBind(self):
        # Finally, build the bind string from what we have left over
        self.Binding = "+".join([ key for key in [self.ModSlot, self.KeySlot] if key])

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
                wx.WXK_WINDOWS_LEFT: '', # TODO - is this OK?  keeps it from blowing up but...
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
                ord('(') : '9',
                ord(')') : '0',
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
