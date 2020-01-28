import json
import os

from src.DataClasses.Data.Files.SoundFXListEntry import SoundFXListEntry
from src.Utilities.FileConverter import FileConverter


class SoundFXList(FileConverter):
    def __init__(self, path):
        super().__init__(path)

        self.soundFXList = []

    def _FileConverter__convert(self):
        while True:
            soundEvent = SoundFXListEntry(self.file.ReadUInt(), self.file.ReadUInt(),
                                          self.file.ReadUInt(), self.file.ReadUInt())

            if (
                    soundEvent.Frame == 0xFFFFFFFF
                    and soundEvent.Sample == 0x00000000
                    and soundEvent.Volume == 0x00000000
                    and soundEvent.Panning == 0x00000000
            ):
                break

            self.soundFXList.append(soundEvent.__dict__)

        self.finish()

    def _FileConverter__save(self, outputPath):
        jsonDump = json.dumps(self.soundFXList)

        with open(outputPath + ".json", "w") as finalFile:
            finalFile.write(jsonDump)

        os.remove(outputPath)
