import os
import json
import logging
import zlib

from PIL import Image

from src.Helpers.logger import *
from src.Utilities import FileConverter

class EpisodeConverter(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.position = 0

        self.episodeToken = os.path.splitext(os.path.basename(path))[0]
        self.episodeName = ""
        self.episodeImage = None
        self.episodeTitleImage = None
        self.firstLevel = ""

        self.isRegistered = False

    
    def convert(self):
        super().convert()

        try:
            self.__readHeader()
            self.__readEpisodeInfo()
            self.__readEpisodeImagesData()
        except Exception as e:
            logging.error(error("Unexpected error happened during conversion of episode file! (" + str(e) + ")"))
            self.finish()
    
    def __readHeader(self):
        headerSize = self.file.ReadUInt()

        self.position = self.file.ReadUInt()
        self.isRegistered = (self.file.ReadUInt() != 0)

        unknown = self.file.ReadUInt()
    
    def __readEpisodeInfo(self):
        """ Episode name"""
        episodeNameRaw = self.file.ReadBytes(128)
        episodeName = episodeNameRaw.decode()

        firstNullByte = episodeName.find("\0")

        if firstNullByte is not -1:
            self.episodeName = episodeName[:firstNullByte]
        
        """ First level """
        firstLevelRaw = self.file.ReadBytes(32)
        firstLevel = firstLevelRaw.decode()

        firstNullByte = firstLevel.find("\0")

        if firstNullByte is not -1:
            self.firstLevel = firstLevel[:firstNullByte]
    
    def __readEpisodeImagesData(self):
        self.width = self.file.ReadUInt()
        self.height = self.file.ReadUInt()

        unknown1 = self.file.ReadUInt()
        unknown2 = self.file.ReadUInt()

        self.titleWidth = self.file.ReadUInt()
        self.titleHeight = self.file.ReadUInt()

        unknown3 = self.file.ReadUInt()
        unknown4 = self.file.ReadUInt()
    
    def __readImage(self, width, height, outputPath):
        imagePackedSize = self.file.ReadUInt()
        imageUnpackedSize = width * height

        imageBlock = zlib.decompress(self.file.ReadBytes(imagePackedSize))

        if len(imageBlock) != imageUnpackedSize:
            logging.error(error("Invalid image unpacked size! "
                                "Expected " + str(imageUnpackedSize) + ", got " + str(len(imageBlock)) +
                                " Skipping that image..."))
            return
        
        try:
            palette = json.loads(open(outputPath.replace("Episodes", "Data") + "/Menu.Palette.json", "r").read())
        except Exception:
            logging.error(error("Cannot find palette file (Data/Menu.Palette.json), will use index colors..."))
            palette = False
        
        image = Image.new("RGBA", [width, height], 255)
        imageData = image.load()

        for y in range(height):
            for x in range(width):
                colorID = imageBlock[y * width + x]

                if palette is not False:
                    color = palette[colorID]
                else:
                    color = {"a": colorID, "r": colorID, "g": colorID, "b": colorID}
                
                imageData[x, y] = (color["r"], color["g"], color["b"], color["a"])
        
        return image
    
    def save(self, outputPath):
        super().save(outputPath)

        try:
            fileLayout = {
                "episodeName": self.episodeName,
                "episodeToken": self.episodeToken,
                "firstlevel": self.firstLevel,
                "isRegistered": self.isRegistered,
                "position": self.position
            }

            outputDir = outputPath + self.episodeName + "/"
            os.mkdir(outputDir)

            with open(outputDir + "episode.json", "w") as episodeFile:
                json.dump(fileLayout, episodeFile)
            
            logging.info(info("Now converting episode image..."))
            self.episodeImage = self.__readImage(self.width, self.height, outputPath)
            self.episodeImage.save(outputDir + "image.png")
            logging.info(info("Now converting episode title image..."))
            self.episodeTitleImage = self.__readImage(self.titleWidth, self.titleHeight, outputPath)
            self.episodeTitleImage.save(outputDir + "title.png")
        except Exception as e:
            logging.error(error("Unexpected error happened while saving episode... (" + str(e) + ")"))
            self.finish()

