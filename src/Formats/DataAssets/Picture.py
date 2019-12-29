import os
import logging

from PIL import Image

from src.Helpers.logger import *
from src.Utilities import FileConverter
from src.DataClasses import Color


class PictureDataFile(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.width = 0
        self.height = 0
        self.bitDepth = 0

        self.palette = []
        self.image = None
        self.imageData = None

    def convert(self):
        super().convert()

        try:
            self.__loadPictureData()
            self.__loadPalette()
            self.__convertImage()
        except Exception as e:
            logging.error(error("Unexpected error happened while converting file: " + self.path + "! (" + str(e) + ")"))

    def __loadPictureData(self):
        self.width = self.file.ReadUInt()
        self.height = self.file.ReadUInt()
        self.bitDepth = self.file.ReadUInt()

        logging.debug(verbose("Picture info: " + str(self.width) + "x" + str(self.height) +
                              " (" + str(self.bitDepth) + " bit depth" + ")"))

    def __loadPalette(self):
        for colorByte in range(256):
            color = Color()

            color.r = self.file.ReadByte()
            color.g = self.file.ReadByte()
            color.b = self.file.ReadByte()
            color.a = self.file.ReadByte()

            self.palette.append(color)

    def __convertImage(self):
        self.image = Image.new("RGBA", [self.width, self.height], 255)
        self.imageData = self.image.load()

        for x in range(self.image.size[1]):
            for y in range(self.image.size[0]):
                imageByte = self.file.ReadByte()
                colorByte = self.palette[imageByte]

                self.imageData[y, x] = (colorByte.r, colorByte.g, colorByte.b, colorByte.a)

        self.finish()

    def save(self, outputPath):
        super().save(outputPath)

        self.image.save(outputPath + ".png")
        os.remove(outputPath)
