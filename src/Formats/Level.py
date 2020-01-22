import logging
import os

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
        self.animCourt = 0
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


    def save(self, outputPath):
        super().save(outputPath)
