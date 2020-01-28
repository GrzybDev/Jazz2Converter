import zlib

from src.Compatibility.Assets.Palette import PaletteDataFile
from src.Compatibility.Assets.Picture import PictureDataFile
from src.Compatibility.Assets.SoundFXList import SoundFXList
from src.Compatibility.Assets.Texture import TextureDataFile
from src.DataClasses.Data.File import DataFile
from src.Logger import error, warning, verbose, info
from src.Utilities.DataBlock import DataBlock
from src.Utilities.FileConverter import FileConverter

knownFileTypes = {
    0x23: PictureDataFile,
    0x18: PictureDataFile,
    0x1D: PictureDataFile,
    0x17: PictureDataFile,
    0x16: PictureDataFile,
    0x19: PictureDataFile,
    0x1A: PictureDataFile,
    0x15: PictureDataFile,
    0x52: PictureDataFile,
    0x9: PaletteDataFile,
    0xFFFFFFFF: PaletteDataFile,
    0x11C9A10: SoundFXList,
    0x11C8330: SoundFXList,
    0x11C88A0: SoundFXList,
    0x11C8750: SoundFXList,
    0x11C8320: SoundFXList,
    0x11C8AB0: TextureDataFile,
}


class DataConverter(FileConverter):
    def __init__(self, path):
        super().__init__(path)

        self.magic: int = 0x0  # Should be: 0x42494C50 (PLIB)
        self.signature: int = 0x0  # Should be 0xBEBAADDE

        self.version: int = 0

        self.recordedSize: int = 0
        self.recordedCRC: int = 0

        self.headerBlock: str = ""

        self.archiveFiles = []
        self.headerEndOffset: int = 0

    def _FileConverter__convert(self):
        self.__checkFile()
        self.__loadData()

        self.__loadHeaderBlock()

    def __checkFile(self):
        self.magic = self.file.ReadUInt()

        if self.magic != 0x42494C50:
            error("File " + self.path + " is not correct Jazz Jackrabbit 2 Data File! (Incorrect magic number)")
            raise ValueError("Invalid magic number")

        self.signature = self.file.ReadUInt()

        if self.signature != 0xBEBAADDE:
            error("File " + self.path + " is not correct Jazz Jackrabbit 2 Data File! (Incorrect signature)")
            raise ValueError("Invalid signature")

    def __loadData(self):
        self.version = self.file.ReadUInt()

        self.recordedSize = self.file.ReadUInt()
        self.recordedCRC = self.file.ReadUInt()

    def __loadHeaderBlock(self):
        headerBlockPackedSize = self.file.ReadUInt()
        headerBlockUnpackedSize = self.file.ReadUInt()
        self.headerBlock = DataBlock(self.file.ReadBytes(headerBlockPackedSize),
                                     headerBlockPackedSize, headerBlockUnpackedSize)

        while True:
            file = DataFile()

            file.name = self.headerBlock.ReadString(32, True)

            if file.name == "":  # Most probably end of header block
                break

            file.type = self.headerBlock.ReadUInt()
            file.offset = self.headerBlock.ReadUInt()
            file.fileCRC = self.headerBlock.ReadUInt()
            file.filePackedSize = self.headerBlock.ReadUInt()
            file.fileUnpackedSize = self.headerBlock.ReadUInt()

            verbose("Found file: " + file.name + " (type: " + str(hex(file.type)) + ") at offset " + str(file.offset) +
                    " (size: " + str(file.filePackedSize) + " bytes)")

            self.archiveFiles.append(file)

        self.headerEndOffset = self.file.context.tell()

    def _FileConverter__save(self, outputPath):
        for file in self.archiveFiles:
            verbose("Decompressing " + file.name + "...")
            finalFilePath = outputPath + file.name

            self.file.context.seek(self.headerEndOffset + file.offset)

            rawFile = self.file.ReadBytes(file.filePackedSize)
            decompressedFile = zlib.decompress(rawFile)

            if len(decompressedFile) != file.fileUnpackedSize:
                warning("Failed to save file to " + finalFilePath + "! " +
                        "That file won't be converted/saved...")
                continue

            fileConverter = knownFileTypes.get(file.type)

            if fileConverter is None:
                warning("Unknown file type: " + str(file.type) + "! " +
                        "Will save raw file to " + finalFilePath)

            with open(finalFilePath, "wb") as finalFile:
                info("Now saving file " + finalFilePath + "...")
                finalFile.write(decompressedFile)
                finalFile.close()

            if fileConverter is not None:
                fileConverter = fileConverter(finalFilePath)
                fileConverter.convert()
                fileConverter.save(finalFilePath)
