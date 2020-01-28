import json
import os

from src.DataClasses.Color import Color
from src.Utilities.FileConverter import FileConverter


class PaletteDataFile(FileConverter):
    def __init__(self, path):
        super().__init__(path)

        self.palette = []

    def _FileConverter__convert(self):
        for byte in range(256):
            color = Color(self.file.ReadByte(), self.file.ReadByte(), self.file.ReadByte(), self.file.ReadByte())
            self.palette.append(color.__dict__)

        self.finish()

    def _FileConverter__save(self, outputPath):
        jsonDump = json.dumps(self.palette)

        with open(outputPath + ".json", "w") as finalFile:
            finalFile.write(jsonDump)

        os.remove(outputPath)
