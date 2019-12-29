import logging
import os

from PIL import Image

from src.Helpers.logger import *
from src.Utilities import FileConverter


class TextureDataFile(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.width, self.height = path.split(".")[-1].split("x")

        self.image = Image.new("RGBA", [int(self.width), int(self.height)], 255)
        self.imageData = self.image.load()

    def convert(self):
        super().convert()

        try:
            for x in range(self.image.size[1]):
                for y in range(self.image.size[0]):
                    imageByte = self.file.ReadByte()

                    self.imageData[y, x] = (imageByte, imageByte, imageByte, imageByte)
        except Exception as e:
            logging.error(error("Unexpected error happened while converting file: " + self.path + "! (" + str(e) + ")"))

        self.finish()

    def save(self, outputPath):
        super().save(outputPath)

        self.image.save(outputPath + ".png")
        os.remove(outputPath)
