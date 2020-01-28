import os

from PIL import Image

from src.DataClasses.Color import Color
from src.DataClasses.Tileset.TileSection import TileSection
from src.Logger import error
from src.Utilities.DataBlock import DataBlock
from src.Utilities.FileConverter import FileConverter


class TilesetConverter(FileConverter):
    def __init__(self, path):
        super().__init__(path)

        self.name: str = ""
        self.palette = []
        self.tiles = []
        self.tileCount: int = 0
        self.maxTilesCount: int = 0

        self.infoBlock = None
        self.imageBlock = None
        self.alphaBlock = None
        self.maskBlock = None

    def _FileConverter__convert(self):
        self.file.ReadBytes(180)  # Skip copyright notice

        self.__readHeader()

        self.__LoadMetadata()
        self.__LoadImageData()
        self.__LoadMaskData()

    def __readHeader(self):
        headerBlock = DataBlock(self.file.ReadBytes(82), 82)

        magicValue = headerBlock.ReadUInt()
        signature = headerBlock.ReadUInt()

        if magicValue == 0x454C4954:
            error("Invalid magic value (Expected " + str(0x454C4954) + ", but got " + str(magicValue) + ")")
            raise ValueError("Invalid magic value")

        if signature == 0xAFBEADDE:
            error("Invalid signature (Expected " + str(0xAFBEADDE) + ", but got " + str(signature) + ")")
            raise ValueError("Invalid signature")

        self.name = headerBlock.ReadString(32, True)
        version = headerBlock.ReadUShort()
        self.maxTilesCount = 1024 if version <= 512 else 4096

        recordedSize = headerBlock.ReadUInt()
        recordedCRC = headerBlock.ReadUInt()

        infoBlockPackedSize = headerBlock.ReadUInt()
        infoBlockUnpackedSize = headerBlock.ReadUInt()
        imageBlockPackedSize = headerBlock.ReadUInt()
        imageBlockUnpackedSize = headerBlock.ReadUInt()
        alphaBlockPackedSize = headerBlock.ReadUInt()
        alphaBlockUnpackedSize = headerBlock.ReadUInt()
        maskBlockPackedSize = headerBlock.ReadUInt()
        maskBlockUnpackedSize = headerBlock.ReadUInt()

        self.infoBlock = DataBlock(self.file.ReadBytes(infoBlockPackedSize),
                                   infoBlockPackedSize, infoBlockUnpackedSize)
        self.imageBlock = DataBlock(self.file.ReadBytes(imageBlockPackedSize),
                                    imageBlockPackedSize, imageBlockUnpackedSize)
        self.alphaBlock = DataBlock(self.file.ReadBytes(alphaBlockPackedSize),
                                    alphaBlockPackedSize, alphaBlockUnpackedSize)
        self.maskBlock = DataBlock(self.file.ReadBytes(maskBlockPackedSize),
                                   maskBlockPackedSize, maskBlockUnpackedSize)

    def __LoadMetadata(self):
        self.palette = [Color(self.infoBlock.ReadByte(), self.infoBlock.ReadByte(), self.infoBlock.ReadByte(),
                              255 - self.infoBlock.ReadByte()) for each in range(256)]

        self.tileCount = self.infoBlock.ReadUInt()
        self.tiles = [TileSection() for each in range(self.maxTilesCount)]

        for tile in self.tiles: tile.Opaque = self.infoBlock.ReadBool()

        self.infoBlock.DiscardBytes(self.maxTilesCount)  # Block of unknown bytes, skip

        for tile in self.tiles: tile.ImageDataOffset = self.infoBlock.ReadUInt()

        self.infoBlock.DiscardBytes(4 * self.maxTilesCount)  # Block of unknown bytes, skip

        for tile in self.tiles: tile.AlphaDataOffset = self.infoBlock.ReadUInt()

        self.infoBlock.DiscardBytes(4 * self.maxTilesCount)  # Block of unknown bytes, skip

        for tile in self.tiles: tile.MaskDataOffset = self.infoBlock.ReadUInt()

        self.infoBlock.DiscardBytes(4 * self.maxTilesCount)

    def __LoadImageData(self):
        blockSize = 32

        for tile in self.tiles:
            tile.Image = Image.new("RGBA", [blockSize, blockSize], 255)
            image = tile.Image.load()

            imageData = self.imageBlock.ReadRawBytes(blockSize * blockSize, tile.ImageDataOffset)
            alphaMaskData = self.alphaBlock.ReadRawBytes(128, tile.AlphaDataOffset)

            for i in range(blockSize * blockSize):
                idx = imageData[i]

                if (
                        len(alphaMaskData) > 0
                        and ((alphaMaskData[int(i / 8)] >> (i % 8)) & 0x01) == 0x00
                ):
                    color = self.palette[0]
                else:
                    color = self.palette[idx]

                image[i % blockSize, i / blockSize] = (
                    color.r,
                    color.g,
                    color.b,
                    color.a,
                )

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
                        mask[pixelIdx % blockSize, pixelIdx / blockSize] = (
                            0, 0, 0, 0)  # Transparent
                    else:
                        mask[pixelIdx % blockSize, pixelIdx / blockSize] = (
                            0, 0, 0, 255)  # Black

    def _FileConverter__save(self, outputPath):
        tileSize = 32
        tilesPerRow = 30

        tilesTexture = Image.new(
            "RGBA",
            [
                tileSize * tilesPerRow,
                int(((self.tileCount - 1) / tilesPerRow + 1)) * tileSize,
            ],
        )
        masksTexture = Image.new(
            "RGBA",
            [
                tileSize * tilesPerRow,
                int(((self.tileCount - 1) / tilesPerRow + 1)) * tileSize,
            ],
        )

        for i in range(self.maxTilesCount):
            tile = self.tiles[i]

            tilesTexture.paste(
                tile.Image,
                ((i % tilesPerRow) * tileSize, int(i / tilesPerRow) * tileSize),
            )
            masksTexture.paste(
                tile.Mask,
                ((i % tilesPerRow) * tileSize, int(i / tilesPerRow) * tileSize),
            )

        outputPath = outputPath + os.path.splitext(os.path.basename(self.path))[0] + "/"
        os.mkdir(outputPath)

        tilesTexture.save(outputPath + "Diffuse.png")
        masksTexture.save(outputPath + "Mask.png")
