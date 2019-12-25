import json
import logging

from src.File import File
from src.logger import *


class LanguageConverter(object):
    def __init__(self, path):
        self.file = File(open(path, "rb"))
        self.path = path

        self.stringsCount = 0

        self.mainBlockLength = 0
        self.mainBlockContent = []

        self.isFinished = False

    def convert(self):
        logging.info(info("Now converting " + self.path + "..."))

        self.__readStringsCount()
        self.__readFirstBlock()

    def save(self, to):
        convertedLayout = {
            "main": self.mainBlockContent
        }

        fileJSON = json.dumps(convertedLayout)

        logging.info(info("Finished conversion. Now saving to " + to + "..."))

        finalFile = open(to, "w")
        finalFile.write(fileJSON)
        finalFile.close()

        self.cancel()

    def cancel(self):
        self.file.context.close()

    def __readStringsCount(self):
        self.stringsCount = self.file.ReadUInt()

        logging.debug(verbose("Strings count: " + str(self.stringsCount)))

    def __readFirstBlock(self):
        self.mainBlockLength = self.file.ReadUInt()

        logging.debug(verbose("Main block length (in bytes): " + str(self.mainBlockLength)))

        endingOffset = self.file.context.tell() + self.mainBlockLength

        for i in range(self.stringsCount):
            if self.file.context.tell() <= endingOffset:  # Check if we are not exceeding main block
                self.mainBlockContent.append(self.file.ReadNullTerminatedString())
            else:
                logging.warning(warning("Current offset is: " + str(self.file.context.tell()) +
                                        ", and main block should end at: " + str(endingOffset) +
                                        ".\nBut there's still " + str(self.stringsCount - i) + " strings left!\n"
                                        "Skipping conversion of that file..."))
                self.cancel()
