import logging
import os
import zlib

from PIL import Image

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
        self.tiles = []
        self.tileCount = 0
        self.maxTilesCount = 0

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

        try:
            self.file.ReadBytes(180)  # Skip copyright notice

            self.__readHeader()

            self.__LoadMetadata()
            self.__LoadImageData()
            self.__LoadMaskData()
        except Exception as e:
            logging.error(error("Unexpected error happened during conversion! (" + str(e) + ")"))
            self.finish()

    def __readHeader(self):
        headerBlock = DataBlock(self.file.ReadBytes(82))

        magicValue = headerBlock.ReadUInt()
        signature = headerBlock.ReadUInt()

        if magicValue == 0x454C4954 and signature == 0xAFBEADDE:
            self.name = headerBlock.ReadString(32, True)
            self.version = headerBlock.ReadUShort()
            self.maxTilesCount = 1024 if self.version <= 512 else 4096
            
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

    def __LoadMetadata(self):
        for i in range(256):
            self.palette.append({
                "R": self.infoBlock.ReadByte(),
                "G": self.infoBlock.ReadByte(),
                "B": self.infoBlock.ReadByte(),
                "A": 255 - self.infoBlock.ReadByte()
            })

        self.tileCount = self.infoBlock.ReadUInt()

        for i in range(self.maxTilesCount):
            self.tiles.append(TileSection())
            self.tiles[i].Opaque = self.infoBlock.ReadBool()

        self.infoBlock.DiscardBytes(self.maxTilesCount)  # Block of unknown bytes, skip

        for i in range(self.maxTilesCount):
            self.tiles[i].ImageDataOffset = self.infoBlock.ReadUInt()

        self.infoBlock.DiscardBytes(4 * self.maxTilesCount)  # Block of unknown bytes, skip

        for i in range(self.maxTilesCount):
            self.tiles[i].AlphaDataOffset = self.infoBlock.ReadUInt()

        self.infoBlock.DiscardBytes(4 * self.maxTilesCount)  # Block of unknown bytes, skip

        for i in range(self.maxTilesCount):
            self.tiles[i].MaskDataOffset = self.infoBlock.ReadUInt()

        self.infoBlock.DiscardBytes(4 * self.maxTilesCount)

    def __LoadImageData(self, usePalette=True):
        blockSize = 32

        for tile in self.tiles:
            tile.Image = Image.new("RGBA", [blockSize, blockSize], 255)
            image = tile.Image.load()

            imageData = self.imageBlock.ReadRawBytes(blockSize * blockSize, tile.ImageDataOffset)
            alphaMaskData = self.alphaBlock.ReadRawBytes(128, tile.AlphaDataOffset)

            for i in range(blockSize * blockSize):
                idx = imageData[i]

                if len(alphaMaskData) > 0 and ((alphaMaskData[int(i / 8)] >> (i % 8)) & 0x01) == 0x00:
                    color = self.palette[0] if usePalette else {"R": 0, "G": 0, "B": 0, "A": 0}
                else:
                    color = self.palette[idx] if usePalette else {"R": idx, "G": idx, "B": idx, "A": 0 if idx == 0 else 255}

                image[i % blockSize, i / blockSize] = (color["R"], color["G"], color["B"], color["A"])

    def __LoadMaskData(self):
        blockSize = 32

        for tile in self.tiles:
            tile.Mask = Image.new("RGBA", [blockSize, blockSize], 255)
            mask = tile.Mask.load()

            maskData = self.maskBlock.ReadRawBytes(128, tile.MaskDataOffset)

            for i in range(128):
                idx = maskData[i]

                for j in range(8):
                    pixelIdx = 8 * i + j

                    if ((idx >> j) & 0x01) == 0:
                        mask[pixelIdx % blockSize, pixelIdx / blockSize] = (0, 0, 0, 0)  # Transparent
                    else:
                        mask[pixelIdx % blockSize, pixelIdx / blockSize] = (0, 0, 0, 255)  # Black

    def save(self, outputPath):
        super().save(outputPath)

        tileSize = 32
        tilesPerRow = 30

        tilesTexture = Image.new("RGBA", [tileSize * tilesPerRow, int(((self.tileCount - 1) / tilesPerRow + 1)) * tileSize])
        masksTexture = Image.new("RGBA", [tileSize * tilesPerRow, int(((self.tileCount - 1) / tilesPerRow + 1)) * tileSize])
        indexTexture = Image.new("RGBA", [tileSize * tilesPerRow, int(((self.tileCount - 1) / tilesPerRow + 1)) * tileSize])

        for i in range(self.maxTilesCount):
            tile = self.tiles[i]

            tilesTexture.paste(tile.Image, ((i % tilesPerRow) * tileSize, int(i / tilesPerRow) * tileSize))
            masksTexture.paste(tile.Mask, ((i % tilesPerRow) * tileSize, int(i / tilesPerRow) * tileSize))

        outputPath = outputPath + os.path.splitext(os.path.basename(self.path))[0] + "/"
        os.mkdir(outputPath)

        tilesTexture.save(outputPath + "Diffuse.png")
        masksTexture.save(outputPath + "Mask.png")

        self.__LoadImageData(usePalette=False)  # Read file again but this time only save indexes of colors (for normal map)
        for i in range(self.maxTilesCount):
            tile = self.tiles[i]

            indexTexture.paste(tile.Image, ((i % tilesPerRow) * tileSize, int(i / tilesPerRow) * tileSize))

        indexTexture.save(outputPath + "Index.png")
