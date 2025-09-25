import pytest
import GameData
import Util.Incarnate

def test_baddata(monkeypatch):
    monkeypatch.setattr(GameData, 'IncarnatePowers', {
        'thingie' : {
            'Types' : {
                'testing' : {
                    'Effects' : [{}],
                    'Levels' : [[{}]]
                },
            },
            'Levels' : ['level one'],
            'Effects' : ['one', 'two'],
        }
    })

    with pytest.raises(Exception, match = f'Something is terribly wrong'):
        Util.Incarnate.BuildSlotData()

