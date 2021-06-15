#  KeyBind mixin -- intended to be mixed into each of page.Controls
# so we can just iterate and create the bind tuples to push into
# bindfiles.

class KeyBind():
    def __init__(self):
        self.KeyBindKey      = ''
        self.KeyBindName     = ''
        self.KeyBindContents = ''

    def GetKeyBindString():
        return f'{self.KeyBindKey} "{self.KeyBindContents}"'

