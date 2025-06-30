import GameData.Homecoming
import GameData.Rebirth

Alignments = [
    'Hero',
    'Villain',
    'Vigilante',
    'Rogue',
    'Resistance',
    'Loyalist',
]

Origins = ['Magic','Mutation','Natural','Science','Technology']

Archetypes = {}
MiscPowers = {}
SprintPowers = []
Inspirations = {}
DefaultBinds = {}
Emotes = {}
IncarnatePowers = {}
PoolPowers = {}

# There's probably a better way to do this.
def SetupGameData(server = "Homecoming"):
    if server == "Rebirth":
        GameData.Archetypes = GameData.Rebirth.Archetypes
        GameData.MiscPowers = GameData.Rebirth.MiscPowers
        GameData.SprintPowers = GameData.Rebirth.SprintPowers
        GameData.Inspirations = GameData.Rebirth.Inspirations
        GameData.DefaultBinds = GameData.Rebirth.DefaultBinds
        GameData.Emotes = GameData.Rebirth.Emotes
        GameData.IncarnatePowers = GameData.Rebirth.IncarnatePowers
        GameData.PoolPowers = GameData.Rebirth.PoolPowers
    else:
        GameData.Archetypes = GameData.Homecoming.Archetypes
        GameData.MiscPowers = GameData.Homecoming.MiscPowers
        GameData.SprintPowers = GameData.Homecoming.SprintPowers
        GameData.Inspirations = GameData.Homecoming.Inspirations
        GameData.DefaultBinds = GameData.Homecoming.DefaultBinds
        GameData.Emotes = GameData.Homecoming.Emotes
        GameData.IncarnatePowers = GameData.Homecoming.IncarnatePowers
        GameData.PoolPowers = GameData.Homecoming.PoolPowers

