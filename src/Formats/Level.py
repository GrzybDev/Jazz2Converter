import logging
import os
import zlib

from src.Helpers.logger import *
from src.Utilities import FileConverter
from src.DataClasses.Level import *
from src.DataClasses.Data import DataBlock


class LevelConverter(FileConverter):

    LayerCount = 8

    def __init__(self, path):
        super().__init__(path)

        self.levelToken, self.name = ("", "")
        self.tileset, self.music = ("", "")
        self.nextLevel, self.bonusLevel, self.secretLevel = ("", "", "")

        self.layers = []
        self.staticTiles = []
        self.animatedTiles = []
        self.events = []

        self.textEventStrings = []
        self.levelTokenTextIDs = []

        self.version = 0
        self.lightingMin, self.lightingStart = (0, 0)
        self.animCount = 0
        self.verticalMPSplitscreen = False
        self.isMpLevel = False
        self.hasPit, self.hasCTF, self.hasLaps = (False, False, False)

    def convert(self):
        super().convert()

        self.file.ReadBytes(180)  # Skip copyright notice

        self.levelToken = os.path.splitext(os.path.basename(self.path))[0]

        self.__ReadHeader()

    def __ReadHeader(self):
        headerBlock = DataBlock(self.file.ReadBytes(82))

        magic = headerBlock.ReadUInt()
        if magic != 0x4C56454C:
            logging.error(error("Invalid magic number in level file!"))
            self.finish()

        self.passwordHash = headerBlock.ReadUInt()
        self.name = headerBlock.ReadString(32, True)

        self.version = headerBlock.ReadUShort()
        self.MaxSupportedTiles = 1024 if self.version <= 514 else 4096
        self.MaxSupportedAnims = 128 if self.version <= 514 else 256

        self.recordedSize = headerBlock.ReadUInt()
        self.recordedCRC = headerBlock.ReadUInt()

        self.infoBlockPackedSize = headerBlock.ReadUInt()
        self.infoBlockUnpackedSize = headerBlock.ReadUInt()
        self.eventBlockPackedSize = headerBlock.ReadUInt()
        self.eventBlockUnpackedSize = headerBlock.ReadUInt()
        self.dictBlockPackedSize = headerBlock.ReadUInt()
        self.dictBlockUnpackedSize = headerBlock.ReadUInt()
        self.layoutBlockPackedSize = headerBlock.ReadUInt()
        self.layoutBlockUnpackedSize = headerBlock.ReadUInt()

        self.infoBlock = self.file.ReadBytes(self.infoBlockPackedSize)
        self.eventBlock = self.file.ReadBytes(self.eventBlockPackedSize)
        self.dictBlock = self.file.ReadBytes(self.dictBlockPackedSize)
        self.layoutBlock = self.file.ReadBytes(self.layoutBlockPackedSize)

        if len(self.infoBlock) != self.infoBlockPackedSize \
                or len(self.eventBlock) != self.eventBlockPackedSize \
                or len(self.dictBlock) != self.dictBlockPackedSize \
                or len(self.layoutBlock) != self.layoutBlockPackedSize:
            logging.error(error("File is incomplete or corrupted!"))
            self.finish()
            return

        self.infoBlock = zlib.decompress(self.infoBlock)
        self.eventBlock = zlib.decompress(self.eventBlock)
        self.dictBlock = zlib.decompress(self.dictBlock)
        self.layoutBlock = zlib.decompress(self.layoutBlock)

        if len(self.infoBlock) != self.infoBlockUnpackedSize \
                or len(self.eventBlock) != self.eventBlockUnpackedSize \
                or len(self.dictBlock) != self.dictBlockUnpackedSize \
                or len(self.layoutBlock) != self.layoutBlockUnpackedSize:
            logging.error(error("Incorrect block sizes after decompression!"))
            self.finish()
            return

        self.infoBlock = DataBlock(self.infoBlock)
        self.eventBlock = DataBlock(self.eventBlock)
        self.dictBlock = DataBlock(self.dictBlock)
        self.layoutBlock = DataBlock(self.layoutBlock)

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
            logging.error(error("Level name mismatch!"))
            self.finish()
            return

        self.tileset = self.infoBlock.ReadString(32, True)
        self.bonusLevel = self.infoBlock.ReadString(32, True)
        self.nextLevel = self.infoBlock.ReadString(32, True)
        self.secretLevel = self.infoBlock.ReadString(32, True)
        self.music = self.infoBlock.ReadString(32, True)

        self.textEventStrings = []

        for i in range(16):
            self.textEventStrings.append(self.infoBlock.ReadString(512, True))

        self.levelTokenTextIDs = []

        self.__LoadLayerMetadata()

        self.staticTilesCount = self.infoBlock.ReadUShort()

        if self.MaxSupportedTiles - self.animCount != self.staticTilesCount:
            logging.error(error("Tile count mismatch!"))
            self.finish()
            return

    def __LoadLayerMetadata(self):
        self.layers = []
        for i in range(self.LayerCount):
            self.layers.append(LayerSection())

        for i in range(self.LayerCount):
            self.layers[i].Flags = self.infoBlock.ReadUInt()

        for i in range(self.LayerCount):
            self.layers[i].Type = self.infoBlock.ReadByte()

        for i in range(self.LayerCount):
            self.layers[i].Used = self.infoBlock.ReadBool()

        for i in range(self.LayerCount):
            self.layers[i].Width = self.infoBlock.ReadUInt()

        for i in range(self.LayerCount):
            self.layers[i].InternalWidth = self.infoBlock.ReadUInt()

        for i in range(self.LayerCount):
            self.layers[i].Height = self.infoBlock.ReadUInt()

        for i in range(self.LayerCount):
            self.layers[i].Depth = self.infoBlock.ReadUInt()

        for i in range(self.LayerCount):
            self.layers[i].DetailLevel = self.infoBlock.ReadByte()

        for i in range(self.LayerCount):
            self.layers[i].WaveX = self.infoBlock.ReadEncodedFloat()

        for i in range(self.LayerCount):
            self.layers[i].WaveY = self.infoBlock.ReadEncodedFloat()

        for i in range(self.LayerCount):
            self.layers[i].SpeedX = self.infoBlock.ReadEncodedFloat()

        for i in range(self.LayerCount):
            self.layers[i].SpeedY = self.infoBlock.ReadEncodedFloat()

        for i in range(self.LayerCount):
            self.layers[i].AutoSpeedX = self.infoBlock.ReadEncodedFloat()

        for i in range(self.LayerCount):
            self.layers[i].AutoSpeedY = self.infoBlock.ReadEncodedFloat()

        for i in range(self.LayerCount):
            self.layers[i].TexturedBackgroundType = self.infoBlock.ReadByte()

        for i in range(self.LayerCount):
            self.layers[i].TexturedParams1 = self.infoBlock.ReadByte()
            self.layers[i].TexturedParams2 = self.infoBlock.ReadByte()
            self.layers[i].TexturedParams3 = self.infoBlock.ReadByte()

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
                tileEvent.EventType = Event(eventData & 0x000000FF)
                tileEvent.Difficulty = (eventData & 0x00000300) == 0
                tileEvent.Illuminate = ((eventData & 0x00000400) >> 10) == 1
                tileEvent.TileParams = (eventData & 0xFFFFF000) >> 12

        if self.events[-1].EventType == Event.MCE:
            self.hasPit = True

        for event in self.events:
            if event.EventType == Event.CTF_BASE:
                self.hasCTF = True
            elif event.EventType == Event.WARP_ORIGIN:
                self.hasLaps = True

    def __LoadLayers(self):
        dictLength = int(self.dictBlockUnpackedSize / 8)
        self.dictionary = [DictionaryEntry() for each in range(dictLength)]

        for entry in self.dictionary:
            for i in range(4):
                entry.Tiles.append(self.dictBlock.ReadUShort())

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

    def save(self, outputPath):
        super().save(outputPath)
