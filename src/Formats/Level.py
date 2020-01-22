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


    def save(self, outputPath):
        super().save(outputPath)
