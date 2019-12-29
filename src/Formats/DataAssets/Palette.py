import os
import logging
import json

from src.Helpers.logger import *
from src.Utilities import FileConverter
from src.DataClasses import Color


class PaletteDataFile(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.palette = []

    def convert(self):
        super().convert()

        try:
            for byte in range(256):
                color = Color()

                color.r = self.file.ReadByte()
                color.g = self.file.ReadByte()
                color.b = self.file.ReadByte()
                color.a = self.file.ReadByte()

                self.palette.append(color.__dict__)
        except Exception as e:
            logging.error(error("Unexpected error happened while converting file: " + self.path + "! (" + str(e) + ")"))

        self.finish()

    def save(self, outputPath):
        super().save(outputPath)

        jsonDump = json.dumps(self.palette)

        with open(outputPath + ".json", "w") as finalFile:
            finalFile.write(jsonDump)

        os.remove(outputPath)
