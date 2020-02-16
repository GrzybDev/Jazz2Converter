import os
import json
from PIL import Image

from src.DataClasses.Color import Color
from src.Logger import error
from src.Utilities.FileConverter import FileConverter


class TexturePalettePatcher(FileConverter):
    def __init__(self, path):
        super().__init__(path)
        self.finish()

        self.image = None
        self.imageData = None
        self.palette = None

    def _FileConverter__convert(self):
        self.image = Image.open(self.path)
        self.imageData = self.image.load()
        
        basePath = self.path.replace(os.path.basename(self.path), "")
        fileName = self.path.replace(basePath, "")
        paletteName = fileName.split(".")[0]
        palettePath = basePath + paletteName + '.Palette.json'

        try:
            with open(palettePath, "r") as pFile:
                pJSON = json.loads(pFile.read())
                self.palette = [Color(colorID["r"], colorID["g"], colorID["b"], colorID["a"]) for colorID in pJSON]
        except Exception as e:
            error("Cannot find palette file (Data/Menu.Palette.json), will use index colors... (" + str(e) + ")")
            return

        for y in range(self.image.height):
            for x in range(self.image.width):
                colorID = self.imageData[x, y][0]
                color = self.palette[colorID]
                self.imageData[x, y] = (color.r, color.g, color.b, color.a)

    def _FileConverter__save(self, outputPath):
        self.image.save(outputPath)
