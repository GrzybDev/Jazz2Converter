import logging
import zlib

from src.Helpers.logger import *
from src.Utilities import FileConverter
from src.DataClasses.Data import *
from src.DataClasses.Tileset import *


class TilesetConverter(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.name = ""
        self.version = 0
        self.palette = []
        self.titles = []
        self.tileCount = 0

        self.recordedSize = 0
        self.recordedCRC = 0

        self.infoBlockPackedSize = 0
        self.infoBlockUnpackedSize = 0
        self.infoBlock = None
        
        self.imageBlockPackedSize = 0
        self.imageBlockUnpackedSize = 0
        self.imageBlock = None

        self.alphaBlockPackedSize = 0
        self.alphaBlockUnpackedSize = 0
        self.alphaBlock = None

        self.maskBlockPackedSize = 0
        self.maskBlockUnpackedSize = 0
        self.maskBlock = None

    
    def convert(self):
        super().convert()

        self.file.ReadBytes(180)  # Skip copyright notice

        self.__readHeader()
    
    def __readHeader(self):
        headerBlock = DataBlock(self.file.ReadBytes(82))

        if (magicValue := headerBlock.ReadUInt()) == 0x454C4954 and (signature := headerBlock.ReadUInt()) == 0xAFBEADDE:
            self.name = headerBlock.ReadString(32, True)
            self.version = headerBlock.ReadUShort()
            
            self.recordedSize = headerBlock.ReadUInt()
            self.recordedCRC = headerBlock.ReadUInt()

            self.infoBlockPackedSize = headerBlock.ReadUInt()
            self.infoBlockUnpackedSize = headerBlock.ReadUInt()
            self.imageBlockPackedSize = headerBlock.ReadUInt()
            self.imageBlockUnpackedSize = headerBlock.ReadUInt()
            self.alphaBlockPackedSize = headerBlock.ReadUInt()
            self.alphaBlockUnpackedSize = headerBlock.ReadUInt()
            self.maskBlockPackedSize = headerBlock.ReadUInt()
            self.maskBlockUnpackedSize = headerBlock.ReadUInt()

            self.infoBlock = self.file.ReadString(self.infoBlockPackedSize)
            self.imageBlock = self.file.ReadString(self.imageBlockPackedSize)
            self.alphaBlock = self.file.ReadString(self.alphaBlockPackedSize)
            self.maskBlock = self.file.ReadString(self.maskBlockPackedSize)

            if len(self.infoBlock) != self.infoBlockPackedSize \
                or len(self.imageBlock) != self.imageBlockPackedSize \
                or len(self.alphaBlock) != self.alphaBlockPackedSize \
                or len(self.maskBlock) != self.maskBlockPackedSize:
                logging.error(error("File is incomplete or corrupted!"))
                self.finish()
                return
            
            self.infoBlock = zlib.decompress(self.infoBlock)
            self.imageBlock = zlib.decompress(self.imageBlock)
            self.alphaBlock = zlib.decompress(self.alphaBlock)
            self.maskBlock = zlib.decompress(self.maskBlock)

            if len(self.infoBlock) != self.infoBlockUnpackedSize \
                or len(self.imageBlock) != self.imageBlockUnpackedSize \
                or len(self.alphaBlock) != self.alphaBlockUnpackedSize \
                or len(self.maskBlock) != self.maskBlockUnpackedSize:
                logging.error(error("Incorrect block sizes after decompression!!"))
                self.finish()
                return
            
            self.infoBlock = DataBlock(self.infoBlock)
            self.imageBlock = DataBlock(self.imageBlock)
            self.alphaBlock = DataBlock(self.alphaBlock)
            self.maskBlock = DataBlock(self.maskBlock)
        else:
            logging.error(error("Tileset header have invalid magic number or signature!"))
            self.finish()

    
    def save(self, outputPath):
        super().save(outputPath)