import logging
import zlib

from src.DataClasses.Data import *
from src.Helpers.logger import *
from src.Utilities.FileConverter import FileConverter


class DataConverter(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.magic = 0x0  # Should be: 0x42494C50 (PLIB)
        self.signature = 0x0  # Should be 0xBEBAADDE

        self.version = 0

        self.recordedSize = 0
        self.recordedCRC = 0

        self.headerBlockPackedSize = 0
        self.headerBlockUnpackedSize = 0
        self.headerBlock = ""

        self.archiveFiles = []

    def convert(self):
        super().convert()

        try:
            self.__checkFile()
            self.__loadData()

            self.__loadHeaderBlock()
        except Exception as e:
            logging.error(error("Unexpected error happened while converting file: " + self.path + "! (" + str(e) + ")"))

    def __checkFile(self):
        self.magic = self.file.ReadUInt()

        if self.magic != 0x42494C50:
            logging.warning(warning("File " + self.path + " is not correct Jazz Jackrabbit 2 Data File!"
                                                          " (Incorrect magic number) "
                                                          "Skipping that file..."))
            self.finish()

        self.signature = self.file.ReadUInt()

        if self.signature != 0xBEBAADDE:
            logging.warning(warning("File " + self.path + " is not correct Jazz Jackrabbit 2 Data File!"
                                                          " (Incorrect signature) "
                                                          "Skipping that file..."))
            self.finish()

    def __loadData(self):
        self.version = self.file.ReadUInt()

        self.recordedSize = self.file.ReadUInt()
        self.recordedCRC = self.file.ReadUInt()

    def __loadHeaderBlock(self):
        self.headerBlockPackedSize = self.file.ReadUInt()
        self.headerBlockUnpackedSize = self.file.ReadUInt()

        self.headerBlock = zlib.decompress(self.file.ReadBytes(self.headerBlockPackedSize))

        if len(self.headerBlock.data) != self.headerBlockUnpackedSize:
            logging.warning(warning("File " + self.path + " is not correct Jazz Jackrabbit 2 Data File!"
                                                          " (Incorrect unpacked size) "
                                                          "Skipping that file..."))
            self.finish()
        else:
            self.headerBlock = DataBlock(self.headerBlock)

        while True:
            file = DataFile()

            file.name = self.headerBlock.ReadString(32, True)

            if file.name == '':  # Most probably end of header block
                break

            file.type = self.headerBlock.ReadUInt()
            file.offset = self.headerBlock.ReadUInt()
            file.fileCRC = self.headerBlock.ReadUInt()
            file.filePackedSize = self.headerBlock.ReadUInt()
            file.fileUnpackedSize = self.headerBlock.ReadUInt()

            logging.debug(verbose("Found file: " + file.name + " (type: " + str(hex(file.type)) + ") at offset " +
                                  str(file.offset) + " (size: " + str(file.filePackedSize) + " bytes)"))

    def save(self, outputPath):
        super().save(outputPath)
