import os

from PIL import Image

from src.DataClasses.Color import Color
from src.Logger import verbose
from src.Utilities.FileConverter import FileConverter


class PictureDataFile(FileConverter):
    def __init__(self, path):
        super().__init__(path)

        self.width = 0
        self.height = 0
        self.bitDepth = 0

        self.palette = []
        self.image = None
        self.imageData = None

    def _FileConverter__convert(self):
        self.__loadPictureData()
        self.__loadPalette()
        self.__convertImage()

        self.finish()

    def __loadPictureData(self):
        self.width = self.file.ReadUInt()
        self.height = self.file.ReadUInt()
        self.bitDepth = self.file.ReadUInt()

        verbose("Picture info: " + str(self.width) + "x" + str(self.height) + " " +
                "(" + str(self.bitDepth) + " bit depth)")

    def __loadPalette(self):
        for colorByte in range(256):
            color = Color(self.file.ReadByte(), self.file.ReadByte(), self.file.ReadByte(), self.file.ReadByte())
            self.palette.append(color)

    def __convertImage(self):
        self.image = Image.new("RGBA", [self.width, self.height], 255)
        self.imageData = self.image.load()

        for x in range(self.image.size[1]):
            for y in range(self.image.size[0]):
                imageByte = self.file.ReadByte()
                colorByte = self.palette[imageByte]

                self.imageData[y, x] = (
                    colorByte.r,
                    colorByte.g,
                    colorByte.b,
                    colorByte.a,
                )

    def _FileConverter__save(self, outputPath):
        self.image.save(outputPath + ".png")
        os.remove(outputPath)
