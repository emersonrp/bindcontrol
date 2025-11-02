import Exceptions
import GameData.Homecoming
import GameData.Rebirth
import Util.Incarnate

Server = ''

# Alignment -> color tuple
Alignments = {
    'Hero'       : ( 35, 130, 212),
    'Villain'    : (225,  65,  65),
    'Vigilante'  : (241, 213, 114),
    'Rogue'      : (180, 180, 180),
    'Resistance' : ( 30, 240, 255),
    'Loyalist'   : (255, 226,  56),
}

Origins = ['Magic','Mutation','Natural','Science','Technology']

Archetypes = {}
MiscPowers = {}
SprintPowers = []
Inspirations = {}
DefaultBinds = {}
Emotes = {}
IncarnatePowers = {}
MMPowerSets = {}
PoolPowers = {}
TempTravelPowers = {}

# There's probably a better way to do this.
def SetupGameData(server):
    GameData.Server = server
    if server == "Rebirth":
        GameData.Archetypes       = GameData.Rebirth.Archetypes
        GameData.MiscPowers       = GameData.Rebirth.MiscPowers
        GameData.SprintPowers     = GameData.Rebirth.SprintPowers
        GameData.Inspirations     = GameData.Rebirth.Inspirations
        GameData.DefaultBinds     = GameData.Rebirth.DefaultBinds
        GameData.Emotes           = GameData.Rebirth.Emotes
        GameData.IncarnatePowers  = GameData.Rebirth.IncarnatePowers
        GameData.MMPowerSets      = GameData.Rebirth.MMPowerSets
        GameData.PoolPowers       = GameData.Rebirth.PoolPowers
        GameData.TempTravelPowers = GameData.Rebirth.TempTravelPowers
    elif server == 'Homecoming':
        GameData.Archetypes       = GameData.Homecoming.Archetypes
        GameData.MiscPowers       = GameData.Homecoming.MiscPowers
        GameData.SprintPowers     = GameData.Homecoming.SprintPowers
        GameData.Inspirations     = GameData.Homecoming.Inspirations
        GameData.DefaultBinds     = GameData.Homecoming.DefaultBinds
        GameData.Emotes           = GameData.Homecoming.Emotes
        GameData.IncarnatePowers  = GameData.Homecoming.IncarnatePowers
        GameData.MMPowerSets      = GameData.Homecoming.MMPowerSets
        GameData.PoolPowers       = GameData.Homecoming.PoolPowers
        GameData.TempTravelPowers = GameData.Homecoming.TempTravelPowers
    else:
        msg = f'GameData.SetupGameData called with unknown server "{server}"'
        raise Exceptions.GameDataBadServerException(msg)

    Util.Incarnate.BuildSlotData()
