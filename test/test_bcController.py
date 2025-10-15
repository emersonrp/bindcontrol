from bcController import bcController

def test_bcController_inits(app): # 'app' to initialize wx.App()
    bcC = bcController()
    assert bcC is not None

def test_bcController_CodeTable(app):
    bcC = bcController()
    assert bcC.CodeTable != []

# TODO, this is ugly hardcoded but will catch any weirdness I guess
def test_bcController_GetAllAxisCodes(app, monkeypatch):
    monkeypatch.setattr(bcController, 'IsOk', lambda _: True)

    monkeypatch.setattr('platform.system', lambda: 'Windows')
    bcC = bcController()
    CodeTable = bcC.GetAllAxisCodes()
    assert CodeTable == [
                    'J1_L', 'J1_R',
                    'J1_U', 'J1_D',
                    'J2_L', 'J2_R',
                    'J3_U', 'J3_D',
                    'J3_L', 'J3_R',
                    'J2_L', 'J2_R',
                    'JP_L', 'JP_R',
                    'JP_U', 'JP_D',
            ]

    monkeypatch.setattr('platform.system', lambda: 'Linux')
    bcC = bcController()
    monkeypatch.setattr(bcC, 'IsOk', lambda: True)
    CodeTable = bcC.GetAllAxisCodes()
    assert CodeTable == [
                    'J1_L', 'J1_R',
                    'J1_U', 'J1_D',
                    'J2_R',
                    'J3_L', 'J3_R',
                    'J3_U', 'J3_D',
                    'J2_L',
                    'JP_L', 'JP_R',
                    'JP_U', 'JP_D',
            ]

    monkeypatch.setattr('platform.system', lambda: 'Darwin')
    bcC = bcController()
    monkeypatch.setattr(bcC, 'IsOk', lambda: True)
    CodeTable = bcC.GetAllAxisCodes()
    assert CodeTable == [
                    'J1_L', 'J1_R',
                    'J1_U', 'J1_D',
                    'J3_L', 'J3_R',
            ]

def test_bcController_AxisPercent(app):
    bcC = bcController()
    assert bcC.AxisPercent(-65535, 65535, 0     ) == 0
    assert bcC.AxisPercent(-65535, 65535, 32768 ) == 50
    assert bcC.AxisPercent(-65535, 65535, -32768) == -50
    assert bcC.AxisPercent(0     , 65535, 32768 ) == 0
    assert bcC.AxisPercent(0     , 65535, 0     ) == -100
    assert bcC.AxisPercent(0     , 65535, 65535 ) == 100

def test_bcController_StickIsNearCenter(app):
    bcC = bcController()
    bcC.CurrentAxisPercents = [0, 0, 0, 0]
    assert bcC.StickIsNearCenter()

    bcC.CurrentAxisPercents = [10, 20, 30, 40]
    assert bcC.StickIsNearCenter()

    bcC.CurrentAxisPercents = [0, 100, 0, 0]
    assert not bcC.StickIsNearCenter()

    bcC.CurrentAxisPercents = [10, 20, 51, 40]
    assert not bcC.StickIsNearCenter()

    bcC.CurrentAxisPercents = [10, 20, -51, 40]
    assert not bcC.StickIsNearCenter()

def test_bcController_ListOfPossibleMods(app, monkeypatch):
    bcC = bcController()
    assert bcC.ListOfPossibleMods() == []

    monkeypatch.setattr(bcC, 'IsOk', lambda: True)
    monkeypatch.setattr(bcC, 'HasPOV4Dir', lambda: False)
    monkeypatch.setattr(bcC, 'GetMaxAxes', lambda: 0)
    assert bcC.ListOfPossibleMods() == ["", "LTrigger", "RTrigger"]

    monkeypatch.setattr(bcC, 'GetNumberButtons', lambda: 4)
    assert bcC.ListOfPossibleMods() == ["", "LTrigger", "RTrigger", "JOY1", "JOY2", "JOY3", "JOY4"]

    monkeypatch.setattr(bcC, 'GetNumberButtons', lambda: 6)
    assert bcC.ListOfPossibleMods() == ["", "LTrigger", "RTrigger", "JOY1", "JOY2", "JOY3", "JOY4", "LeftBumper", "RightBumper"]

    monkeypatch.setattr(bcC, 'GetNumberButtons', lambda: 0)

    monkeypatch.setattr(bcC, 'HasPOV4Dir', lambda: True)
    assert bcC.ListOfPossibleMods() == ["", "LTrigger", "RTrigger", "Joypad_Up", "Joypad_Down", "Joypad_Left", "Joypad_Right"]

    monkeypatch.setattr(bcC, 'HasPOV4Dir', lambda: False)
    monkeypatch.setattr(bcC, 'GetMaxAxes', lambda: 8)
    assert bcC.ListOfPossibleMods() == ["", "LTrigger", "RTrigger", "Joypad_Up", "Joypad_Down", "Joypad_Left", "Joypad_Right"]

def test_bcController_GetCurrentAxis_POV4Dir(app, monkeypatch):
    bcC = bcController()
    monkeypatch.setattr(bcC, 'HasPOV4Dir', lambda: True)
    assert bcC.GetCurrentAxis() == ''

    monkeypatch.setattr(bcC, 'GetPOVPosition', lambda: 0)
    assert bcC.GetCurrentAxis() == "JP_U"

    monkeypatch.setattr(bcC, 'GetPOVPosition', lambda: 9000)
    assert bcC.GetCurrentAxis() == "JP_R"

    monkeypatch.setattr(bcC, 'GetPOVPosition', lambda: 18000)
    assert bcC.GetCurrentAxis() == "JP_D"

    monkeypatch.setattr(bcC, 'GetPOVPosition', lambda: 27000)
    assert bcC.GetCurrentAxis() == "JP_L"
