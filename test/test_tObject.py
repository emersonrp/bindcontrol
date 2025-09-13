from Models.tObject import tObject

def test_togon():
    t = tObject(FakeProfile('Homecoming'))
    assert t.togon == 'powexectoggleon'
    t = tObject(FakeProfile('Rebirth'))
    assert t.togon == 'px_tgon'

def test_togoff():
    t = tObject(FakeProfile('Homecoming'))
    assert t.togoff == 'powexectoggleoff'
    t = tObject(FakeProfile('Rebirth'))
    assert t.togoff == 'px_tgof'

def test_KeyState():
    t = tObject(FakeProfile('Homecoming'))
    t.X = 1
    t.S = 1
    t.A = 1
    assert t.KeyState() == '010110'
    p = {'toggle' : 'S'}
    assert t.KeyState(p) == '010010'

def test_dirs():
    t = tObject(FakeProfile('Homecoming'))
    t.dow  = f'$$down 1'
    t.forw = f'$$forw 1'
    t.rig  = f'$$right 1'

    assert t.dirs('UDFBLR') == "$$down 1$$forw 1$$right 1"

class FakeProfile(object):
    def __init__(self, server):
        self.ServerName = server

    def Server(self):
        return self.ServerName
