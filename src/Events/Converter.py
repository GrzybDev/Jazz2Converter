from src.DataClasses.Event import Event
from src.Events.EventConverter import EventConverter
from src.Events.EventParamType import EventParamType
from src.Mappings.Events.EventType import EventType

event = Event()


class Converter:

    @staticmethod
    def Airboard(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 5]])  # Delay - Default: 30 (sec)

        event.Type = EventType.AirboardGenerator
        event.Params = [30 if eventParams[0] == 0 else eventParams[0], 0, 0, 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def AreaEOL(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.Bool, 1],  # Secret
                                                              [EventParamType.Bool, 1],  # Fast (JJ2+)
                                                              [EventParamType.UInt, 4],  # TextID (JJ2+)
                                                              [EventParamType.UInt, 4]])  # Offset (JJ2+)

        if eventParams[2] != 0:
            level.AddLevelTokenTextID(eventParams[2])

        event.Type = EventType.AreaEndOfLevel
        event.Params = [4 if eventParams[0] == 1 else 1, eventParams[1], eventParams[2], eventParams[3], 0]
        return event

    @staticmethod
    def AreaEOLWarp(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.Bool, 1],  # Empty (JJ2+)
                                                              [EventParamType.Bool, 1],  # Fast (JJ2+)
                                                              [EventParamType.UInt, 4],  # TextID (JJ2+)
                                                              [EventParamType.UInt, 4]])  # Offset (JJ2+)

        if eventParams[2] != 0:
            level.AddLevelTokenTextID(eventParams[2])

        event.Type = EventType.AreaEndOfLevel
        event.Params = [2, eventParams[1], eventParams[2], eventParams[3], 0]
        return event

    @staticmethod
    def AreaLimitXScroll(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Left (Tiles)
                                                              [EventParamType.UInt, 10]])  # Right (Tiles)

        event.Type = EventType.ModifierLimitCameraView
        event.Params = [eventParams[0], eventParams[1], 0, 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def AreaNoFire(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 2],  # Set To (JJ2+)
                                                              [EventParamType.UInt, 2]])  # Var (JJ2+)

        event.Type = EventType.AreaNoFire
        event.Params = [eventParams[0], eventParams[1], eventParams[2]]
        return event

    @staticmethod
    def AreaSecretWarp(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Coins
                                                              [EventParamType.UInt, 4],  # TextID (JJ2+)
                                                              [EventParamType.UInt, 4]])  # Offset (JJ2+)

        if eventParams[1] != 0:
            level.AddLevelTokenTextID(eventParams[1])

        event.Type = EventType.AreaEndOfLevel
        event.Params = [3, 0, eventParams[1], eventParams[2], eventParams[0]]
        return event

    @staticmethod
    def AreaText(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 8],  # Text
                                                              [EventParamType.Bool, 1],  # Vanish
                                                              [EventParamType.Bool, 1],  # AngelScript (JJ2+)
                                                              [EventParamType.UInt, 8]])  # Offset (JJ2+)

        event.Type = EventType.AreaCallback if eventParams[2] != 0 else EventType.AreaText
        event.Params = [eventParams[0], eventParams[3], eventParams[1]]
        return event

    @staticmethod
    def BallSpike3D(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 2],  # Sync
                                                              [EventParamType.Int, 6],  # Speed
                                                              [EventParamType.UInt, 4],  # Length
                                                              [EventParamType.Bool, 1],  # Swing
                                                              [EventParamType.Bool, 1]])  # Shade

        event.Type = EventType.SpikeBall
        event.Params = [eventParams[0], eventParams[1], eventParams[2], eventParams[3], eventParams[4]]
        return event

    @staticmethod
    def Birdy(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.Bool, 1]])  # Chuck (Yellow)

        event.Type = EventType.BirdCage
        event.Params = [eventParams[0], 0]
        return event

    @staticmethod
    def BossDevanRobot(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 4],  # IntroText
                                                              [EventParamType.UInt, 4]])  # EndText

        event.Type = EventType.BossDevanRemote
        event.Params = [0, eventParams[0], eventParams[1], 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def Bridge(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 4],  # Width
                                                              [EventParamType.UInt, 3],  # Type
                                                              [EventParamType.UInt, 4]])  # Toughness

        event.Type = EventType.Bridge
        event.Params = [eventParams[0] * 2, eventParams[1], eventParams[2], 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def ConstantParamList(ev, *eventParams, level, params):
        event.Type = ev
        event.Params = [param for param in eventParams]
        return event

    @staticmethod
    def CrateBomb(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 8],  # ExtraEvent
                                                              [EventParamType.UInt, 4],  # NumEvent
                                                              [EventParamType.Bool, 1],  # RandomFly
                                                              [EventParamType.Bool, 1]])  # NoBomb

        event.Type = EventType.Crate

        if eventParams[0] > 0 and eventParams[1] > 0:
            event.Params = [eventParams[0], eventParams[1]]
        elif eventParams[3] == 0:
            event.Params = [int(EventType.Bomb), 1]
        else:
            event.Params = [0, 0]

        return event

    @staticmethod
    def EOLSign(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.Bool, 1]])  # Secret

        event.Type = EventType.SignEOL
        event.Params = [4 if eventParams[0] == 1 else 1, 0, 0, 0, 0]
        return event

    @staticmethod
    def GetAmmoCrateConverter(Type, level, params):
        event.Type = EventType.CrateAmmo
        event.Params = [Type, 0, 0, 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def GetBossConverter(ev, level, params, customParam=0):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 4]])  # EndText

        event.Type = ev
        event.Params = [customParam, eventParams[0], 0, 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def GetPlatformConverter(type, level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 2],  # Sync
                                                              [EventParamType.Int, 6],  # Speed
                                                              [EventParamType.UInt, 4],  # Length
                                                              [EventParamType.Bool, 1]])  # Swing

        event.Type = EventType.MovingPlatform
        event.Params = [type, eventParams[0], eventParams[1], eventParams[2], eventParams[3], 0, 0, 0]
        return event

    @staticmethod
    def GetPoleConverter(theme, level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 5],  # Adjust X
                                                              [EventParamType.Int, 6]])  # Adjust Y

        AdjustX, AdjustY = (2, 2)
        x, y = (eventParams[1] + 16 - AdjustX, (24 if eventParams[0] == 0 else eventParams[0]) - AdjustY)

        event.Type = EventType.Pole
        event.Params = [theme, x, y]
        return event

    @staticmethod
    def GetSpringConverter(type, horizontal, frozen, level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.Bool, 1],  # Orientation (vertical only)
                                                              [EventParamType.Bool, 1],  # Keep X Speed (vertical only)
                                                              [EventParamType.Bool, 1],  # Keep Y Speed
                                                              [EventParamType.UInt, 4],  # Delay
                                                              [EventParamType.Bool, 1]])  # Reverse (horizontal only)

        event.Type = EventType.Spring
        event.Params = [type, (5 if eventParams[4] != 0 else 4) if horizontal else eventParams[0] * 2,
                        eventParams[1], eventParams[2], eventParams[3], 1 if frozen else 0, 0, 0]
        return event

    @staticmethod
    def GemRing(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 5],  # Length
                                                              [EventParamType.UInt, 5],  # Speed
                                                              [EventParamType.Bool, 8]])  # Event

        event.Type = EventType.GemRing
        event.Params = [eventParams[0], eventParams[1]]
        return event

    @staticmethod
    def LightFlicker(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 8]])  # Sample

        event.Type = EventType.LightFlicker
        event.Params = [110, 40, 60, 110, 0, 0, 0, 0]
        return event

    @staticmethod
    def LightPulse(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 8],  # Speed
                                                              [EventParamType.UInt, 4],  # Sync
                                                              [EventParamType.UInt, 3],  # Type
                                                              [EventParamType.UInt, 5]])  # Size

        radiusNear1 = 20 if eventParams[3] == 0 else eventParams[3] * 4.8
        radiusNear2 = radiusNear1 * 2
        radiusFar = radiusNear1 * 2.4
        speed = 6 if eventParams[0] == 0 else eventParams[0]
        sync = eventParams[1]

        if eventParams[2] == 4:  # Bright normal light
            event.Type = EventType.LightPulse
            event.Params = [255, 200, radiusNear1, radiusNear2, radiusFar, speed, sync, 0]
        elif eventParams[2] == 5:  # Laser shield/Illuminate Surroundings
            event.Type = EventType.LightIlluminate
            event.Params = [1 if eventParams[1] < 1 else eventParams[1], 0, 0, 0, 0, 0, 0, 0]
        else:  # Normal
            event.Type = EventType.LightPulse
            event.Params = [255, 10, radiusNear1, radiusNear2, radiusFar, speed, sync, 0]

        return event

    @staticmethod
    def LightSteady(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 3],  # Type
                                                              [EventParamType.UInt, 7]])  # Size

        if eventParams[0] == 1:  # Single point (ignores the "Size" parameter)
            event.Type = EventType.LightSteady
            event.Params = [127, 10, 0, 16, 0, 0, 0, 0]
        elif eventParams[0] == 2:  # Single point (brighter) (ignores the "Size" parameter)
            event.Type = EventType.LightSteady
            event.Params = [255, 200, 0, 16, 0, 0, 0, 0]
        elif eventParams[0] == 3:  # Flicker light
            radiusNear = 60 if eventParams[1] == 0 else eventParams[1] * 6
            radiusFar = radiusNear * 1.666

            event.Type = EventType.LightFlicker
            event.Params = [min(110 + eventParams[1] * 2, 255), 40, radiusNear, radiusFar, 0, 0, 0, 0]
        elif eventParams[0] == 4:  # Bright normal light
            radiusNear = 80 if eventParams[1] == 0 else eventParams[1] * 7
            radiusFar = radiusNear * 1.25

            event.Type = EventType.LightFlicker
            event.Params = [255, 200, radiusNear, radiusFar, 0, 0, 0, 0]
        elif eventParams[0] == 5:  # Laser shield/Illuminate Surroundings
            event.Type = EventType.LightIlluminate
            event.Params = [1 if eventParams[1] < 1 else eventParams[1], 0, 0, 0, 0, 0, 0, 0]
        else:  # Normal
            radiusNear = 60 if eventParams[1] == 0 else eventParams[1] * 6
            radiusFar = radiusNear * 1.666

            event.Type = EventType.LightSteady
            event.Params = [255, 10, radiusNear, radiusFar, 0, 0, 0, 0]

        return event

    @staticmethod
    def ModifierAccBelt(isRight, level, params):
        if params == 0:
            params = 3

        event.Type = EventType.AreaHForce
        event.Params = [0, 0, params if not isRight else 0, params if isRight else 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def ModifierBelt(isRight, level, params):
        if params == 0:
            left = 3 if not isRight else 0
            right = 3 if isRight else 0
        elif params > 127:
            left = 0 if not isRight else 256 - params
            right = 0 if isRight else 256 - params
        else:
            left = params if not isRight else 0
            right = params if isRight else 0

        event.Type = EventType.AreaHForce
        event.Params = [left, right, 0, 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def ModifierSetWater(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 8],  # Height (Tiles)
                                                              [EventParamType.Bool, 1],  # Instant
                                                              [EventParamType.UInt, 2]])  # Lightning

        event.Type = EventType.ModifierSetWater
        event.Params = [eventParams[0] * 32, eventParams[1], eventParams[2], 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def ModifierSlide(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 2]])  # Strength

        event.Type = EventType.ModifierSlide
        event.Params = [eventParams[0]]
        return event

    @staticmethod
    def ModifierTube(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.Int, 7],  # X Speed
                                                              [EventParamType.Int, 7],  # Y Speed
                                                              [EventParamType.UInt, 1],  # Trig Sample
                                                              [EventParamType.Bool, 1],  # BecomeNoClip (JJ2+)
                                                              [EventParamType.Bool, 1],  # Noclip Only (JJ2+)
                                                              [EventParamType.UInt, 3]])  # Wait Time (JJ2+)

        event.Type = EventType.ModifierTube
        event.Params = [eventParams[0], eventParams[1], eventParams[5], eventParams[2], eventParams[3], eventParams[4]]
        return event

    @staticmethod
    def ModifierWindLeft(level, params):
        if params > 127:
            left = 256 - params
            right = 0
        else:
            left = 0
            right = params

        event.Type = EventType.AreaHForce
        event.Params = [0, 0, 0, 0, left, right, 0, 0]
        return event

    @staticmethod
    def ModifierWindRight(level, params):
        event.Type = EventType.AreaHForce
        event.Params = [0, 0, 0, 0, 0, params, 0, 0]
        return event

    @staticmethod
    def NoParamList(ev, level, params):
        event.Type = ev
        event.Params = None
        return event

    @staticmethod
    def ParamIntToParamList(ev, *paramDefs, level, params):
        paramDefs = [param for param in paramDefs]
        eventParams = EventConverter.ConvertParamInt(params, paramDefs)

        event.Type = ev
        event.Params = eventParams
        return event

    @staticmethod
    def PowerupSwap(level, params):
        event.Type = EventType.PowerUpMorph
        event.Params = [1]
        return event

    @staticmethod
    def SavePoint(level, params):
        theme = 1 if level.tileset.find("xmas") != -1 else 0

        event.Type = EventType.Checkpoint
        event.Params = [theme, 0]
        return event

    @staticmethod
    def SceneryBubbler(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 4]])  # Speed

        event.Type = EventType.AreaAmbientBubbles
        event.Params = [(eventParams[0] + 1) * 5 / 3, 0, 0, 0, 0, 0, 0, 0]
        return event

    @staticmethod
    def SceneryCollapse(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Wait time
                                                              [EventParamType.UInt, 5]])  # FPS

        event.Type = EventType.SceneryCollapse
        event.Params = [eventParams[0] * 25, eventParams[1]]
        return event

    @staticmethod
    def SceneryDestructEvent(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Empty
                                                              [EventParamType.UInt, 5],  # Speed
                                                              [EventParamType.UInt, 4]])  # Weapon

        if eventParams[1] > 0:
            event.Type = EventType.SceneryDestructSpeed
            event.Params = [eventParams[1]]
        else:
            event.Type = EventType.SceneryDestruct
            event.Params = [eventParams[2]]

        return event

    @staticmethod
    def Snow(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 2],  # Intensity
                                                              [EventParamType.Bool, 1],  # Outdoors
                                                              [EventParamType.Bool, 1],  # Off
                                                              [EventParamType.UInt, 2]])  # Type
        event.Type = EventType.AreaWeather
        event.Params = [0 if eventParams[2] == 1 else eventParams[3] + 1, (eventParams[0] + 1) * 5 / 3, eventParams[1],
                        0, 0, 0, 0, 0]
        return event

    @staticmethod
    def TriggerCrate(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 5],  # Trigger ID
                                                              [EventParamType.Bool, 1],  # Set to (0 - off, 1 - on)
                                                              [EventParamType.Bool, 1]])  # Switch

        event.Type = EventType.TriggerCrate
        event.Params = [eventParams[0], 1 if eventParams[0] == 0 else 0, eventParams[2]]
        return event

    @staticmethod
    def WarpOrigin(level, params):
        eventParams = EventConverter.ConvertParamInt(params, [[EventParamType.UInt, 8],  # Warp ID
                                                              [EventParamType.UInt, 8],  # Coins
                                                              [EventParamType.Bool, 1],  # Set Lap
                                                              [EventParamType.Bool, 1],  # Show
                                                              [EventParamType.Bool, 1]])  # Fast (JJ2+)

        if eventParams[1] > 0 or eventParams[3] != 0:
            event.Type = EventType.WarpCoinBonus
            event.Params = [eventParams[0], eventParams[4], eventParams[2], eventParams[1], eventParams[3]]
        else:
            event.Type = EventType.WarpOrigin
            event.Params = [eventParams[0], eventParams[4], eventParams[2]]

        return event
