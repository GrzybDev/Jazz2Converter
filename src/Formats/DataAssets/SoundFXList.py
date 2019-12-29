import logging
import json
import os

from src.Helpers.logger import *
from src.Utilities import FileConverter
from src.DataClasses.Data.Files import SoundFXListEntry


class SoundFXList(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.soundFXList = []

    def convert(self):
        super().convert()

        try:
            while True:
                soundEvent = SoundFXListEntry()

                soundEvent.frame = self.file.ReadUInt()
                soundEvent.sample = self.file.ReadUInt()
                soundEvent.volume = self.file.ReadUInt()
                soundEvent.panning = self.file.ReadUInt()

                if soundEvent.frame == 0xFFFFFFFF \
                    and soundEvent.sample == 0x00000000 \
                    and soundEvent.volume == 0x00000000 \
                    and soundEvent.panning == 0x00000000:
                    break

                self.soundFXList.append(soundEvent.__dict__)
        except Exception as e:
            logging.error(error("Unexpected error happened while converting file: " + self.path + "! (" + str(e) + ")"))

        self.finish()

    def save(self, outputPath):
        super().save(outputPath)

        jsonDump = json.dumps(self.soundFXList)

        with open(outputPath + ".json", "w") as finalFile:
            finalFile.write(jsonDump)

        os.remove(outputPath)
