import json
import logging

from pathlib import Path

from src.DataClasses.Language import LevelEntry, HelpStringEntry
from src.Helpers.logger import *
from src.Utilities import FileConverter


class LanguageConverter(FileConverter):

    jazz2Encoding = "                                 " \
                    "!\"#$% ^()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                    "[\\]∞_`abcdefghijklmnopqrstuvwxyz" \
                    "   ~   ‚ „…    Š Œ             š œ  Ÿ ¡ęóąśłżźćńĘÓĄŚŁŻŹĆŃ           " \
                    "¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"

    def __init__(self, path):
        super().__init__(path)

        self.stringsCount = 0

        self.mainBlockLength = 0
        self.mainBlockContent = None
        self.mainBlockStringsOffsets = []
        self.mainBlockStrings = []

        self.levelsCount = 0
        self.levelEntries = []

        self.helpStringsBlockLength = 0
        self.helpStringsBlock = None

    def convert(self):
        super().convert()

        try:
            self.__readMainBlock()
            self.__readLevelBlock()
            self.__readHelpStringsBlock()
        except Exception as e:
            logging.error(error("Unexpected error happened while converting file: " + self.path + "! (" + str(e) + ")"))

    def save(self, to):
        finalFilePath = to + Path(self.path).stem + ".json"

        super().save(finalFilePath)

        try:
            convertedLayout = {
                "main": self.mainBlockStrings,
                "levels": self.levelEntries
            }

            with open(finalFilePath, "w", encoding='utf-8') as finalFile:
                json.dump(convertedLayout, finalFile, ensure_ascii=False)

            self.finish()
        except Exception as e:
            logging.error(error("Unexpected error happened while saving to file: " + finalFilePath + "! "
                                "(" + str(e) + ")"))

    def __readStringFromBlock(self, block, offset):
        charCount = 0
        temp = ""

        while True:
            try:
                char = block[offset:][charCount]
            except IndexError:
                char = 0

            if char == 0:
                break
            elif self.jazz2Encoding[char] == "ż":
                nextChar = block[offset:][charCount + 1]
                nextCharEncoded = self.jazz2Encoding[nextChar]

                if nextCharEncoded.isdigit():
                    temp += "^" + nextCharEncoded
                else:
                    temp += "ż" + nextCharEncoded

                charCount += 2
                continue

            temp += self.jazz2Encoding[char]
            charCount += 1

        return temp

    def __readMainBlock(self):
        self.stringsCount = self.file.ReadUInt()
        self.mainBlockLength = self.file.ReadUInt()

        logging.debug(verbose("Strings count: " + str(self.stringsCount)))
        logging.debug(verbose("Main block length (in bytes): " + str(self.mainBlockLength)))
        
        self.mainBlockContent = self.file.ReadBytes(self.mainBlockLength)

        for i in range(self.stringsCount):
            self.mainBlockStringsOffsets.append(self.file.ReadUInt())
        
        logging.debug(verbose("Main block strings offsets: " + str(self.mainBlockStringsOffsets)))

        for offset in self.mainBlockStringsOffsets:
            self.mainBlockStrings.append(self.__readStringFromBlock(self.mainBlockContent, offset))

    def __readLevelEntry(self):
        entry = LevelEntry()

        entry.levelName = self.file.ReadString(8).decode().replace("\x00", "")
        entry.minTextID = self.file.ReadByte()
        entry.maxTextID = self.file.ReadByte()
        entry.levelOffset = self.file.ReadUShort()
        entry.helpStrings = []

        return entry.__dict__

    def __readLevelBlock(self):
        self.levelsCount = self.file.ReadUInt()

        logging.debug(verbose("Level count: " + str(self.levelsCount)))

        for i in range(self.levelsCount):
            self.levelEntries.append(self.__readLevelEntry())

    def __readHelpStringEntry(self, stopAtID, offset):
        currentID = 0

        helpEntries = []

        while stopAtID != currentID:
            entry = HelpStringEntry()

            entry.textID = self.helpStringsBlock[offset:][0]
            currentID = entry.textID
            offset += 1

            entry.textLength = self.helpStringsBlock[offset:][0]
            offset += 1

            helpString = self.helpStringsBlock[offset:][:entry.textLength]
            entry.helpString = self.__readStringFromBlock(helpString, 0)
            offset += entry.textLength

            helpEntries.append(entry.__dict__)

        return helpEntries

    def __readHelpStringsBlock(self):
        self.helpStringsBlockLength = self.file.ReadUInt()
        self.helpStringsBlock = self.file.ReadBytes(self.helpStringsBlockLength)

        for level in self.levelEntries:
            level["helpStrings"].append(self.__readHelpStringEntry(level["maxTextID"], level["levelOffset"]))
