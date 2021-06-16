#  KeyBind mixin -- intended to be mixed into each of page.Controls
# so we can just iterate and create the bind tuples to push into
# bindfiles.

class KeyBind():
    def __init__(self, key, name, page, *contents):
        self.KeyBindKey      = key # actual key combo
        self.KeyBindName     = name # friendly name, ie, "Select All Pets"
        self.KeyBindTab      = page # which tab the bind originated on
        self.KeyBindContents = contents #the actual bindstring (without surrounding "")

    def GetKeyBindString():
        return f'{self.KeyBindKey} "{self.KeyBindContents}"'

