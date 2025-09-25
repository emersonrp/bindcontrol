from Models.tObject import tObject
import wx, pytest

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

def test_blf(config):
    t = tObject(FakeProfile('Homecoming'))
    assert t.BLF('AJ') == "bindloadfilesilent c:\\TestPath\\AJ\\AJ000000.txt"

    t.X = 1
    t.S = 1
    t.D = 1
    assert t.BLF('sm') == "bindloadfilesilent c:\\TestPath\\SM\\SM010101.txt"

    t.space = 1
    t.W = 1
    t.A = 1
    assert t.BLF('sf', 's') == "bindloadfilesilent c:\\TestPath\\SF\\SF111111s.txt"

#####
@pytest.fixture
def config():
    _ = wx.App()
    config = wx.FileConfig()

    yield config

    config.DeleteAll()

class FakeProfile(object):
    def __init__(self, server):
        self.ServerName = server

    def Server(self):
        return self.ServerName

    def BLF(self, *bits):
        return "bindloadfilesilent c:\\TestPath\\" + "\\".join(bits)
