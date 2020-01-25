from src.DataClasses.Event import Event
from src.Mappings import EventParamType
from src.Mappings.EventType import EventType
from src.Mappings.Jazz2Event import Jazz2Event
from functools import partial


class EventConverter:

    def __init__(self):
        self.converters = {}

        self.__AddDefaultConverters()

    def __AddDefaultConverters(self):
        self.__Add(Jazz2Event.EMPTY, partial(self.__NoParamList, EventType.Empty))

        # Basic events
        self.__Add(Jazz2Event.JAZZ_LEVEL_START, partial(self.__ConstantParamList, EventType.LevelStart, 0x01))
        self.__Add(Jazz2Event.SPAZ_LEVEL_START, partial(self.__ConstantParamList, EventType.LevelStart, 0x02))
        self.__Add(Jazz2Event.LORI_LEVEL_START, partial(self.__ConstantParamList, EventType.LevelStart, 0x04))

        self.__Add(Jazz2Event.MP_LEVEL_START, partial(self.__ParamIntToParamList,
                                                      EventType.LevelStartMultiplayer,
                                                      [EventParamType.UInt, 2]))

        self.__Add(Jazz2Event.SAVE_POINT, partial(self.__SavePoint))

        # Scenery events
        self.__Add(Jazz2Event.SCENERY_DESTRUCT, partial(self.__SceneryDestructEvent))
        self.__Add(Jazz2Event.SCENERY_DESTR_BOMB, partial(self.__ConstantParamList, EventType.SceneryDestruct, 7))
        self.__Add(Jazz2Event.SCENERY_BUTTSTOMP, partial(self.__NoParamList, EventType.SceneryDestructButtstomp))
        self.__Add(Jazz2Event.SCENERY_COLLAPSE, partial(self.__SceneryCollapse))

    def __Add(self, old, converter):
        self.converters[old] = converter

    def Convert(self, level, old, eventParams):
        converter = self.converters.get(old)

        if converter is not None:
            return converter(level=level, params=eventParams)
        else:
            event = Event()
            event.Type = EventType.Empty
            event.Params = None
            return event

    @staticmethod
    def ConvertParamInt(paramInt, paramTypes):
        eventParams = [0 for each in range(len(paramTypes))]

        for index, paramType in enumerate(paramTypes):
            if paramType[1] == 0:
                continue

            if paramType[0] == EventParamType.Bool:
                eventParams[index] = paramInt % 2
                paramInt = paramInt >> 1
            elif paramType[0] == EventParamType.UInt:
                eventParams[index] = paramInt % (1 << paramType[1])
                paramInt = paramInt >> paramType[1]
            elif paramType[0] == EventParamType.Int:
                val = paramInt % (1 << paramType[1] - 1)

                # Complement of two, with variable bit length
                highestBitValue = 1 << (paramType[1] - 1)

                if val >= highestBitValue:
                    val = -highestBitValue + (val - highestBitValue)

                eventParams[index] = val
                paramInt = paramInt >> paramType[1]
            else:
                raise ValueError("Invalid paramType! (" + str(paramType[0]) + ")")

        return eventParams

    def __NoParamList(self, ev, level, params):
        event = Event()
        event.Type = ev
        event.Params = None
        return event

    def __ConstantParamList(self, ev, eventParams, level, params):
        event = Event()
        event.Type = ev
        event.Params = [eventParams]
        return event

    def __ParamIntToParamList(self, ev, *paramDefs, level, params):
        paramDefs = [param for param in paramDefs]
        eventParams = self.ConvertParamInt(params, paramDefs)

        event = Event()
        event.Type = ev
        event.Params = eventParams
        return event

    def __SavePoint(self, level, params):
        theme = 1 if level.tileset.find("xmas") != -1 else 0

        event = Event()
        event.Type = EventType.Checkpoint
        event.Params = [theme, 0]
        return event

    def __SceneryDestructEvent(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Empty
                                                    [EventParamType.UInt, 5],   # Speed
                                                    [EventParamType.UInt, 4]])  # Weapon
        event = Event()

        if eventParams[1] > 0:
            event.Type = EventType.SceneryDestructSpeed
            event.Params = [eventParams[1]]
        else:
            event.Type = EventType.SceneryDestruct
            event.Params = [eventParams[2]]

        return event

    def __SceneryCollapse(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Wait time
                                                    [EventParamType.UInt, 5]])  # FPS

        event = Event()
        event.Type = EventType.SceneryCollapse
        event.Params = [eventParams[0] * 25, eventParams[1]]
        return event
