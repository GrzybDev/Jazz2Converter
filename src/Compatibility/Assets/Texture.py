import os

from PIL import Image

from src.Utilities.FileConverter import FileConverter


class TextureDataFile(FileConverter):
    def __init__(self, path):
        super().__init__(path)

        self.width, self.height = path.split(".")[-1].split("x")

        self.image = Image.new("RGBA", [int(self.width), int(self.height)], 255)
        self.imageData = self.image.load()

    def _FileConverter__convert(self):
        for x in range(self.image.size[1]):
            for y in range(self.image.size[0]):
                imageByte = self.file.ReadByte()

                self.imageData[y, x] = (imageByte, imageByte, imageByte, imageByte)

        self.finish()

    def _FileConverter__save(self, outputPath):
        self.image.save(outputPath + ".png")
        os.remove(outputPath)
