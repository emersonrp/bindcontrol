import os
import Util.BuildFiles
from pathlib import Path

def test_BuildFiles():
    fixture = Path(os.path.abspath(__file__)).parent / 'fixtures' / 'buildfile.txt'

    data = Util.BuildFiles.ParseBuildFile(fixture)

    assert data['Name'] == 'Fixture'
    assert data['Archetype'] == 'Tanker'
    assert data['Origin'] == 'Magic'
    assert data['Server'] == 'Homecoming'
    assert data['Primary'] == 'Fiery Aura'
    assert data['Secondary'] == 'War Mace'
    assert data['Pool1'] == 'Flight'
    assert data['Pool2'] == 'Fighting'
    assert data['Pool3'] == 'Leadership'
    assert data['Epic'] == 'Soul Mastery'
