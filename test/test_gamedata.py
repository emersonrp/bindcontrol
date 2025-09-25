import GameData
import pytest

def test_GameData_BadServer():
    with pytest.raises(Exception, match = 'unknown server'):
        GameData.SetupGameData('No Such Server')

def test_GameData_Homecoming():
    GameData.SetupGameData('Homecoming')

    assert isinstance(GameData.Archetypes, dict)
    assert sorted(GameData.Archetypes.keys()) == [
        'Arachnos Soldier', 'Arachnos Widow', 'Blaster', 'Brute', 'Controller',
        'Corruptor', 'Defender', 'Dominator', 'Mastermind', 'Peacebringer',
        'Scrapper', 'Sentinel', 'Stalker', 'Tanker', 'Warshade'
    ]
    for n, a in GameData.Archetypes.items():
        assert isinstance(n, str)
        assert isinstance(a['Primary'], dict)
        assert isinstance(a['Secondary'], dict)
        assert isinstance(a['Epic'], dict)
        assert len(a['Primary']) > 0
        for p in a['Primary'].values():
            assert isinstance(p, list)
            assert len(p) > 0
        assert len(a['Secondary']) > 0
        for s in a['Secondary'].values():
            assert isinstance(s, list)
            assert len(s) > 0
        if n != 'Peacebringer' and n != 'Warshade':
            assert len(a['Epic']) > 0
            for e in a['Epic'].values():
                assert isinstance(e, list)
                assert len(e) > 0

    for n, p in GameData.PoolPowers.items():
        assert isinstance(n, str)
        assert isinstance(p, list)
        assert len(p) > 0

    assert isinstance(GameData.TempTravelPowers, list)
    assert isinstance(GameData.MiscPowers, dict)
    assert isinstance(GameData.SprintPowers, list)

    assert isinstance(GameData.Inspirations, dict)
    assert sorted(GameData.Inspirations) == ['Dual', 'DualTeam', 'Single', 'Team']
    for insp in GameData.Inspirations.values():
        for i in insp.values():
            assert isinstance(i, dict)
            assert 'ltcolor' in i
            assert isinstance(i['ltcolor'], tuple)
            assert 'dkcolor' in i
            assert isinstance(i['dkcolor'], tuple)
            assert 'tiers' in i
            assert isinstance(i['tiers'], list)

def test_GameData_Rebirth():
    GameData.SetupGameData('Rebirth')

    assert isinstance(GameData.Archetypes, dict)
    assert sorted(GameData.Archetypes.keys()) == [
        'Arachnos Soldier', 'Arachnos Widow', 'Blaster', 'Brute', 'Controller',
        'Corruptor', 'Defender', 'Dominator', 'Guardian', 'Mastermind',
        'Peacebringer', 'Scrapper', 'Stalker', 'Tanker', 'Warshade'
    ]
    for n, a in GameData.Archetypes.items():
        assert isinstance(n, str)
        assert isinstance(a['Primary'], dict)
        assert isinstance(a['Secondary'], dict)
        assert isinstance(a['Epic'], dict)
        assert len(a['Primary']) > 0
        for p in a['Primary'].values():
            assert isinstance(p, list)
            assert len(p) > 0
        assert len(a['Secondary']) > 0
        for s in a['Secondary'].values():
            assert isinstance(s, list)
            assert len(s) > 0
        if n != 'Peacebringer' and n != 'Warshade':
            assert len(a['Epic']) > 0
            for e in a['Epic'].values():
                assert isinstance(e, list)
                assert len(e) > 0

    for n, p in GameData.PoolPowers.items():
        assert isinstance(n, str)
        assert isinstance(p, list)
        assert len(p) > 0

    assert isinstance(GameData.TempTravelPowers, list)
    assert isinstance(GameData.MiscPowers, dict)
    assert isinstance(GameData.SprintPowers, list)

    assert isinstance(GameData.Inspirations, dict)
    assert sorted(GameData.Inspirations) == ['Dual', 'DualTeam', 'Single', 'Team']
    for insp in GameData.Inspirations.values():
        for i in insp.values():
            assert isinstance(i, dict)
            assert 'ltcolor' in i
            assert isinstance(i['ltcolor'], tuple)
            assert 'dkcolor' in i
            assert isinstance(i['dkcolor'], tuple)
            assert 'tiers' in i
            assert isinstance(i['tiers'], list)
