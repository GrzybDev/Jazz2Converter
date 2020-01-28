import os
from struct import pack

from src.DataClasses.Level.AnimatedTileSection import AnimatedTileSection
from src.DataClasses.Level.DictionaryEntry import DictionaryEntry
from src.DataClasses.Level.LayerSection import LayerSection
from src.DataClasses.Level.TileEventSection import TileEventSection
from src.DataClasses.Level.TilePropertiesSection import TilePropertiesSection
from src.Events import EventParamType
from src.Events.EventConverter import EventConverter
from src.Logger import error, warning
from src.Mappings.Events.EventType import EventType
from src.Mappings.Events.Jazz2Event import Jazz2Event
from src.Utilities.FileConverter import FileConverter
from src.Utilities.DataBlock import DataBlock

eventConverter = EventConverter()


class LevelConverter(FileConverter):
    LayerCount = 8

    def __init__(self, path):
        super().__init__(path)

        self.levelToken, self.name = (str, str)
        self.tileset, self.music = (str, str)
        self.nextLevel, self.bonusLevel, self.secretLevel = (str, str, str)
        self.passwordHash: str = ""

        self.layers = []
        self.staticTiles = []
        self.animatedTiles = []
        self.events = []

        self.textEventStrings = []
        self.levelTokenTextIDs = []

        self.lightingMin, self.lightingStart = (int, int)
        self.animCount: int = 0
        self.verticalMPSplitscreen: bool = False
        self.isMpLevel: bool = False
        self.hasPit, self.hasCTF, self.hasLaps = (bool, bool, bool)

    def _FileConverter__convert(self):
        self.file.ReadBytes(180)  # Skip copyright notice

        self.levelToken = os.path.splitext(os.path.basename(self.path))[0]

        self.__ReadHeader()

        self.__LoadMetadata()
        self.__LoadEvents()
        self.__LoadLayers()

    def __ReadHeader(self):
        headerBlock = DataBlock(self.file.ReadBytes(82), 82)

        magic = headerBlock.ReadUInt()
        if magic != 0x4C56454C:
            error("Invalid magic number in level file! (Expected " + str(0x4C56454C) + ", but got: " + str(magic) + ")")
            raise ValueError("Invalid magic number in level file!")

        self.passwordHash = headerBlock.ReadUInt()
        self.name = headerBlock.ReadString(32, True)

        version = headerBlock.ReadUShort()
        self.MaxSupportedTiles = 1024 if version <= 514 else 4096
        self.MaxSupportedAnims = 128 if version <= 514 else 256

        recordedSize = headerBlock.ReadUInt()
        recordedCRC = headerBlock.ReadUInt()

        infoBlockPackedSize = headerBlock.ReadUInt()
        infoBlockUnpackedSize = headerBlock.ReadUInt()
        eventBlockPackedSize = headerBlock.ReadUInt()
        eventBlockUnpackedSize = headerBlock.ReadUInt()
        dictBlockPackedSize = headerBlock.ReadUInt()
        dictBlockUnpackedSize = headerBlock.ReadUInt()
        layoutBlockPackedSize = headerBlock.ReadUInt()
        layoutBlockUnpackedSize = headerBlock.ReadUInt()

        self.infoBlock = DataBlock(self.file.ReadBytes(infoBlockPackedSize), infoBlockPackedSize, infoBlockUnpackedSize)
        self.eventBlock = DataBlock(self.file.ReadBytes(eventBlockPackedSize), eventBlockPackedSize,
                                    eventBlockUnpackedSize)
        self.dictBlock = DataBlock(self.file.ReadBytes(dictBlockPackedSize), dictBlockPackedSize, dictBlockUnpackedSize)
        self.layoutBlock = DataBlock(self.file.ReadBytes(layoutBlockPackedSize), layoutBlockPackedSize,
                                     layoutBlockUnpackedSize)

    def __LoadMetadata(self):
        self.infoBlock.DiscardBytes(9)  # First 9 bytes are JCS coordinates on last save

        self.lightingMin = self.infoBlock.ReadByte()
        self.lightingStart = self.infoBlock.ReadByte()

        self.animCount = self.infoBlock.ReadUShort()

        self.verticalMPSplitscreen = self.infoBlock.ReadBool()
        self.isMpLevel = self.infoBlock.ReadBool()

        headerSize = self.infoBlock.ReadUInt()
        secondLevelName = self.infoBlock.ReadString(32, True)

        if secondLevelName != self.name:
            error("Level name mismatch!")
            raise ValueError("Level name mismatch!")

        self.tileset = self.infoBlock.ReadString(32, True)
        self.bonusLevel = self.infoBlock.ReadString(32, True)
        self.nextLevel = self.infoBlock.ReadString(32, True)
        self.secretLevel = self.infoBlock.ReadString(32, True)
        self.music = self.infoBlock.ReadString(32, True)

        self.textEventStrings = [self.infoBlock.ReadString(512, True) for each in range(16)]

        self.levelTokenTextIDs = []

        self.__LoadLayerMetadata()

        self.staticTilesCount = self.infoBlock.ReadUShort()

        if self.MaxSupportedTiles - self.animCount != self.staticTilesCount:
            error("Tile count mismatch!")
            raise ValueError("Tile count mismatch")

        self.__LoadStaticTileData()
        self.infoBlock.DiscardBytes(self.MaxSupportedTiles)  # The unused XMask field
        self.__LoadAnimatedTiles()

    def __LoadLayerMetadata(self):
        self.layers = [LayerSection() for each in range(self.LayerCount)]

        for layer in self.layers: layer.Flags = self.infoBlock.ReadUInt()
        for layer in self.layers: layer.Type = self.infoBlock.ReadByte()
        for layer in self.layers: layer.Used = self.infoBlock.ReadBool()
        for layer in self.layers: layer.Width = self.infoBlock.ReadUInt()
        for layer in self.layers: layer.InternalWidth = self.infoBlock.ReadUInt()
        for layer in self.layers: layer.Height = self.infoBlock.ReadUInt()
        for layer in self.layers: layer.Depth = self.infoBlock.ReadUInt()
        for layer in self.layers: layer.DetailLevel = self.infoBlock.ReadByte()
        for layer in self.layers: layer.WaveX = self.infoBlock.ReadEncodedFloat()
        for layer in self.layers: layer.WaveY = self.infoBlock.ReadEncodedFloat()
        for layer in self.layers: layer.SpeedX = self.infoBlock.ReadEncodedFloat()
        for layer in self.layers: layer.SpeedY = self.infoBlock.ReadEncodedFloat()
        for layer in self.layers: layer.AutoSpeedX = self.infoBlock.ReadEncodedFloat()
        for layer in self.layers: layer.AutoSpeedY = self.infoBlock.ReadEncodedFloat()
        for layer in self.layers: layer.TexturedBackgroundType = self.infoBlock.ReadByte()

        for i in range(self.LayerCount):
            self.layers[i].TexturedParams1 = self.infoBlock.ReadByte()
            self.layers[i].TexturedParams2 = self.infoBlock.ReadByte()
            self.layers[i].TexturedParams3 = self.infoBlock.ReadByte()

    def __LoadStaticTileData(self):
        self.staticTiles = []

        for i in range(self.MaxSupportedTiles):
            self.staticTiles.append(TilePropertiesSection())
            tile = self.staticTiles[i]

            tileEvent = self.infoBlock.ReadUInt()

            tile.Event = TileEventSection()
            tile.Event.EventType = Jazz2Event(tileEvent & 0x000000FF)
            tile.Event.Difficulty = (tileEvent & 0x0000C000) >> 14
            tile.Event.Illuminate = (tileEvent & 0x00002000) >> 13 == 1
            tile.Event.TileParams = ((tileEvent >> 12) & 0x000FFFF0) | ((tileEvent >> 8) & 0x0000000F)

        for i in range(self.MaxSupportedTiles): self.staticTiles[i].Flipped = self.infoBlock.ReadBool()
        for i in range(self.MaxSupportedTiles): self.staticTiles[i].Type = self.infoBlock.ReadByte()

    def __LoadAnimatedTiles(self):
        self.animatedTiles = []

        for i in range(self.animCount):
            self.animatedTiles.append(AnimatedTileSection())
            tile = self.animatedTiles[i]

            tile.Delay = self.infoBlock.ReadUShort()
            tile.DelayJitter = self.infoBlock.ReadUShort()
            tile.ReverseDelay = self.infoBlock.ReadUShort()
            tile.IsReverse = self.infoBlock.ReadBool()
            tile.Speed = self.infoBlock.ReadByte()
            tile.FrameCount = self.infoBlock.ReadByte()

            tile.Frames = []
            for j in range(64):
                tile.Frames.append(self.infoBlock.ReadUShort())

    def __LoadEvents(self):
        width = self.layers[3].Width
        height = self.layers[3].Height

        self.events = [TileEventSection() for each in range(width * height)]

        if width <= 0 and height <= 0:
            return

        for y in range(height):
            for x in range(width):
                eventData = self.eventBlock.ReadUInt()

                tileEvent = self.events[x + y * width]
                tileEvent.EventType = Jazz2Event(eventData & 0x000000FF)
                tileEvent.Difficulty = (eventData & 0x00000300) == 0
                tileEvent.Illuminate = ((eventData & 0x00000400) >> 10) == 1
                tileEvent.TileParams = (eventData & 0xFFFFF000) >> 12

        if self.events[-1].EventType == Jazz2Event.MCE:
            self.hasPit = True

        for event in self.events:
            if event.EventType == Jazz2Event.CTF_BASE:
                self.hasCTF = True
            elif event.EventType == Jazz2Event.WARP_ORIGIN:
                self.hasLaps = True

    def __LoadLayers(self):
        dictLength = int(self.dictBlockUnpackedSize / 8)
        self.dictionary = [DictionaryEntry() for each in range(dictLength)]

        for entry in self.dictionary:
            entry.Tiles = [0 for each in range(4)]

            for i in range(4):
                entry.Tiles[i] = self.dictBlock.ReadUShort()

        for layer in self.layers:
            layer.Tiles = [0 for each in range(layer.InternalWidth * layer.Height)]

            if layer.Used:
                for y in range(layer.Height):
                    for x in range(0, layer.InternalWidth, 4):
                        dictIdx = self.layoutBlock.ReadUShort()
                        tiles = self.dictionary[dictIdx].Tiles

                        for i in range(4):
                            if i + x >= layer.Width:
                                break

                            layer.Tiles[i + x + y * layer.InternalWidth] = tiles[i]

    def _FileConverter__save(self, outputPath):
        outputPath = outputPath + os.path.splitext(os.path.basename(self.path))[0] + "/"
        os.mkdir(outputPath)

        for i in range(len(self.layers)):
            self.__WriteLayer(outputPath + str(i) + ".layer", self.layers[i])

        self.__WriteEvents(outputPath + "Events.data")
        self.__WriteAnimatedTiles(outputPath + "Animated.Tiles")

    def __WriteLayer(self, outputPath, layer):
        if not layer.Used:
            return

        with open(outputPath, "wb") as layerFile:
            maxTiles = self.MaxSupportedTiles
            lastTilesetTileIndex = maxTiles - self.animCount

            layerFile.write(pack("I", layer.Width))
            layerFile.write(pack("I", layer.Height))

            for y in range(layer.Height):
                for x in range(layer.Width):
                    tileIdx = layer.Tiles[x + y * layer.InternalWidth]

                    flipX, flipY = (False, False)
                    if (tileIdx & 0x2000) != 0:
                        flipY = True
                        tileIdx -= 0x2000

                    if (tileIdx & ~(maxTiles | (maxTiles - 1))) != 0:
                        # Fix of bug in updated Psych2.j2l
                        tileIdx = (tileIdx & (maxTiles | (maxTiles - 1))) | maxTiles

                    if (tileIdx & maxTiles) > 0:
                        flipX = True
                        tileIdx -= maxTiles

                    animated = False
                    if tileIdx >= lastTilesetTileIndex:
                        animated = True
                        tileIdx -= lastTilesetTileIndex

                    legacyTranscluent = False
                    invisible = False

                    if not animated and tileIdx < lastTilesetTileIndex:
                        legacyTranscluent = self.staticTiles[tileIdx].Type == 1
                        invisible = self.staticTiles[tileIdx].Type == 3

                    tileFlags = 0
                    if flipX:
                        tileFlags |= 0x01

                    if flipY:
                        tileFlags |= 0x02

                    if animated:
                        tileFlags |= 0x04

                    if legacyTranscluent:
                        tileFlags |= 0x10
                    elif invisible:
                        tileFlags |= 0x20

                    layerFile.write(pack("H", tileIdx))
                    layerFile.write(pack("B", tileFlags))

    def __WriteEvents(self, outputPath):
        width = self.layers[3].Width
        height = self.layers[3].Height

        with open(outputPath, "wb") as eventFile:
            eventFile.write(pack("I", width))
            eventFile.write(pack("I", height))

            for y in range(height):
                for x in range(width):
                    tileEvent = self.events[x + y * width]

                    flags = 0

                    if tileEvent.Illuminate:
                        flags |= 0x04  # Illuminate

                    if tileEvent.Difficulty != 2:
                        flags |= 0x10  # Difficulty: Easy

                    if tileEvent.Difficulty == 0:
                        flags |= 0x20  # Difficulty: Normal

                    if tileEvent.Difficulty != 1:
                        flags |= 0x30  # Difficulty: Hard

                    if tileEvent.Difficulty == 3:
                        flags |= 0x80  # Multiplayer only

                    if tileEvent.EventType == Jazz2Event.MODIFIER_GENERATOR:
                        # Generators are converted diffirently
                        eventParams = EventConverter.ConvertParamInt(
                            tileEvent.TileParams,
                            [
                                [EventParamType.UInt, 8],  # Event
                                [EventParamType.UInt, 8],  # Delay
                                [EventParamType.Bool, 1],
                            ],
                        )  # Initial Delay
                        eventType = Jazz2Event(eventParams[0])
                        generatorDelay = eventParams[1]
                        generatorFlags = eventParams[2]
                    else:
                        eventType = Jazz2Event(tileEvent.EventType)
                        generatorDelay = -1
                        generatorFlags = 0

                    converted = eventConverter.Convert(self, eventType, tileEvent.TileParams)

                    # If the event is unsupported or can't be converted, show warning
                    if (
                            eventType != Jazz2Event.EMPTY
                            and converted.Type == EventType.Empty
                    ):
                        logging.warning(
                            "Unsupported event found in map "
                            + self.levelToken
                            + " ("
                            + str(eventType)
                            + ")!"
                        )

                    eventFile.write(pack("H", int(converted.Type)))

                    if converted.Params is None or all(param == 0 for param in converted.Params):
                        if generatorDelay == -1:
                            eventFile.write(pack("B", flags | 0x01))
                        else:
                            eventFile.write(pack("B", flags | 0x01 | 0x02))
                            eventFile.write(pack("B", generatorFlags))
                            eventFile.write(pack("B", generatorDelay))
                    else:
                        if generatorDelay == -1:
                            eventFile.write(pack("B", flags))
                        else:
                            eventFile.write(pack("B", flags | 0x02))
                            eventFile.write(pack("B", generatorFlags))
                            eventFile.write(pack("B", generatorDelay))

                        if len(converted.Params) > 8:
                            raise ValueError("Event parameter count must be at most 8")

                        fillerBytesCount = 8
                        for i in range(min(len(converted.Params), 8)):
                            eventFile.write(pack("H", int(converted.Params[i])))
                            fillerBytesCount -= 1

                        for i in range(fillerBytesCount):
                            eventFile.write(pack("H", 0))

    def __WriteAnimatedTiles(self, outputPath):
        maxTiles = self.MaxSupportedTiles
        lastTilesetTileIndex = maxTiles - self.animCount

        with open(outputPath, "wb") as tilesFile:
            tilesFile.write(pack("I", len(self.animatedTiles)))

            for tile in self.animatedTiles:
                tilesFile.write(pack("H", tile.FrameCount))

                for i in range(tile.FrameCount):
                    flipX, flipY = (False, False)
                    tileIdx = tile.Frames[i]

                    if (tileIdx & maxTiles) > 0:
                        flipX = True
                        tileIdx -= maxTiles

                    if tileIdx >= lastTilesetTileIndex:
                        fixFrames = self.animatedTiles[tileIdx - lastTilesetTileIndex].Frames
                        warning("Level " + str(self.levelToken) + " has animated tile in animated tile " +
                                "(" + str(tileIdx - lastTilesetTileIndex) + " -> " + str(fixFrames[0]) + ")! " +
                                "Applying quick tile redirection.")
                        tileIdx = fixFrames[0]

                    tileFlags = 0x00

                    if flipX:
                        tileFlags |= 0x01  # Flip X

                    if flipY:
                        tileFlags |= 0x02  # Flip Y

                    if self.staticTiles[tile.Frames[i]].Type == 1:
                        tileFlags |= 0x10  # Legacy Transcluent
                    elif self.staticTiles[tile.Frames[i]].Type == 3:
                        tileFlags |= 0x20  # Invisible

                    tilesFile.write(pack("H", tileIdx))
                    tilesFile.write(pack("B", tileFlags))

                reverse = 1 if tile.IsReverse else 0
                tilesFile.write(pack("B", tile.Speed))
                tilesFile.write(pack("H", tile.Delay))
                tilesFile.write(pack("H", tile.DelayJitter))
                tilesFile.write(pack("B", reverse))
                tilesFile.write(pack("H", tile.ReverseDelay))
