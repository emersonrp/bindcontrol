#  KeyBind mixin -- intended to be mixed into each of page.Controls
# so we can just iterate and create the bind tuples to push into
# bindfiles.

class KeyBind():
    def __init__(self):
        self.KeyBindKey      = '' # actual key combo
        self.KeyBindName     = '' # friendly name, ie, "Select All Pets"
        self.KeyBindContents = '' # the actual bindstring (without surrounding "")

    def GetKeyBindString():
        return f'{self.KeyBindKey} "{self.KeyBindContents}"'

