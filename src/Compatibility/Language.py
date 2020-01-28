import json
from pathlib import Path

from src.DataClasses.Language.HelpStringEntry import HelpStringEntry
from src.DataClasses.Language.LevelEntry import LevelEntry
from src.Logger import verbose
from src.Utilities.FileConverter import FileConverter


class LanguageConverter(FileConverter):
    jazz2Encoding = (
        "                                 "
        '!"#$% ^()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        "[\\]∞_`abcdefghijklmnopqrstuvwxyz"
        "   ~   ‚ „…    Š Œ             š œ  Ÿ ¡ęóąśłżźćńĘÓĄŚŁŻŹĆŃ           "
        "¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"
    )

    def __init__(self, path):
        super().__init__(path)

        self.mainBlockStringsOffsets = []
        self.mainBlockStrings = []

        self.levelEntries = []

    def _FileConverter__convert(self):
        self.__readMainBlock()
        self.__readLevelBlock()
        self.__readHelpStringsBlock()

    def _FileConverter__save(self, to):
        finalFilePath = to + Path(self.path).stem + ".json"

        convertedLayout = {
            "main": self.mainBlockStrings,
            "levels": self.levelEntries,
        }

        with open(finalFilePath, "w", encoding="utf-8") as finalFile:
            json.dump(convertedLayout, finalFile, ensure_ascii=False)

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
        stringsCount = self.file.ReadUInt()
        mainBlockLength = self.file.ReadUInt()

        verbose("Strings count: " + str(stringsCount))
        verbose("Main block length (in bytes): " + str(mainBlockLength))

        mainBlockContent = self.file.ReadBytes(mainBlockLength)
        self.mainBlockStringsOffsets = [self.file.ReadUInt() for each in range(stringsCount)]

        verbose("Main block strings offsets: " + str(self.mainBlockStringsOffsets))

        for offset in self.mainBlockStringsOffsets:
            self.mainBlockStrings.append(self.__readStringFromBlock(mainBlockContent, offset))

    def __readLevelEntry(self):
        entry = LevelEntry()

        entry.levelName = self.file.ReadString(8).decode().replace("\x00", "")
        entry.minTextID = self.file.ReadByte()
        entry.maxTextID = self.file.ReadByte()
        entry.levelOffset = self.file.ReadUShort()
        entry.helpStrings = []

        return entry.__dict__

    def __readLevelBlock(self):
        levelsCount = self.file.ReadUInt()

        verbose("Level count: " + str(levelsCount))

        self.levelEntries = [self.__readLevelEntry() for each in range(levelsCount)]

    def __readHelpStringEntry(self, block, stopAtID, offset):
        currentID = 0

        helpEntries = []

        while stopAtID != currentID:
            entry = HelpStringEntry()

            entry.textID = block[offset:][0]
            currentID = entry.textID
            offset += 1

            entry.textLength = block[offset:][0]
            offset += 1

            helpString = block[offset:][: entry.textLength]
            entry.helpString = self.__readStringFromBlock(helpString, 0)
            offset += entry.textLength

            helpEntries.append(entry.__dict__)

        return helpEntries

    def __readHelpStringsBlock(self):
        helpStringsBlockLength = self.file.ReadUInt()
        helpStringsBlock = self.file.ReadBytes(helpStringsBlockLength)

        for level in self.levelEntries:
            level["helpStrings"].append(
                self.__readHelpStringEntry(helpStringsBlock, level["maxTextID"], level["levelOffset"])
            )
