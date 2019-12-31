import logging
import zlib

from src.Helpers.logger import *
from src.Utilities import FileConverter
from src.DataClasses.Anims import *
from src.DataClasses.Data.Block import DataBlock


class AnimsConverter(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.magic = 0  # Should be ALIB
        self.signature = 0

        self.headerLength = 0
        self.unknownMagic = 0

        self.fileLength = 0
        self.fileCRC = 0

        self.setCount = 0
        self.setAddresses = []

        self.sets = []

    def convert(self):
        super().convert()

        try:
            self.__checkFile()
            self.__loadHeader()

            self.__loadSets()

            for setObj in self.sets:
                self.__loadAnims(setObj)

                self.__convertAnims(setObj)
        except Exception as e:
            logging.error(error("Unexpected error happened while converting file: " + self.path + "! (" + str(e) + ")"))

    def __checkFile(self):
        self.magic = self.file.ReadUInt()
        self.signature = self.file.ReadUInt()

        if self.magic != 0x42494C41:
            logging.warning(warning("Invalid magic number in Anims file! (Expected: " + str(0x42494C41) + ", "
                            "got: " + str(self.magic) + "). Skipping that file..."))
            self.finish()

        if self.signature != 0x00BEBA00:
            logging.warning(warning("Invalid signature in Anims file! (Expected: " + str(0x00BEBA00) + ", "
                            "got: " + str(self.signature) + "). Skipping that file..."))
            self.finish()

    def __loadHeader(self):
        self.headerLength = self.file.ReadUInt()
        self.unknownMagic = self.file.ReadUInt()

        self.fileLength = self.file.ReadUInt()
        self.fileCRC = self.file.ReadUInt()

        self.setCount = self.file.ReadUInt()
        self.__loadSetAddresses()

        logging.debug(verbose("Anim file contains " + str(self.setCount) + " sets!"))
        logging.debug(verbose("Set addresses: " + str(self.setAddresses)))

        if self.headerLength != self.file.context.tell():
            logging.warning(warning("Header length is incorrect (Finished reading header at: " +
                                    str(self.file.context.tell()) + ", but expected to finish it at: " +
                                    str(self.headerLength) + ")"))

    def __loadSetAddresses(self):
        for setID in range(self.setCount):
            self.setAddresses.append(self.file.ReadUInt())

    def __loadSets(self):
        for setID in range(self.setCount):
            animSet = Set()

            magic = self.file.ReadUInt()

            if magic != 0x4D494E41:
                logging.warning(warning("Header for set " + str(setID) + " is incorrect (bad magic value!) "
                                        "Skipping that set..."))
                continue

            animSet.ID = setID

            animSet.animationsCount = self.file.ReadByte()
            animSet.soundsCount = self.file.ReadByte()
            animSet.frameCount = self.file.ReadUShort()
            animSet.cumulativeSoundIndex = self.file.ReadUInt()

            animSet.infoBlockLengthCompressed = self.file.ReadUInt()
            animSet.infoBlockLengthUncompressed = self.file.ReadUInt()
            animSet.frameDataBlockLengthCompressed = self.file.ReadUInt()
            animSet.frameDataBlockLengthUncompressed = self.file.ReadUInt()
            animSet.imageDataBlockLengthCompressed = self.file.ReadUInt()
            animSet.imageDataBlockLengthUncompressed = self.file.ReadUInt()
            animSet.sampleDataBlockLengthCompressed = self.file.ReadUInt()
            animSet.sampleDataBlockLengthUncompressed = self.file.ReadUInt()

            animSet.infoBlock = self.file.ReadBytes(animSet.infoBlockLengthCompressed)
            animSet.frameDataBlock = self.file.ReadBytes(animSet.frameDataBlockLengthCompressed)
            animSet.imageDataBlock = self.file.ReadBytes(animSet.imageDataBlockLengthCompressed)
            animSet.sampleDataBlock = self.file.ReadBytes(animSet.sampleDataBlockLengthCompressed)

            animSet.infoBlock = zlib.decompress(animSet.infoBlock)
            animSet.frameDataBlock = zlib.decompress(animSet.frameDataBlock)
            animSet.imageDataBlock = zlib.decompress(animSet.imageDataBlock)
            animSet.sampleDataBlock = zlib.decompress(animSet.sampleDataBlock)

            if len(animSet.infoBlock) != animSet.infoBlockLengthUncompressed:
                logging.warning(warning("Info block length in set " + str(setID) + " is incorrect (expected " +
                                        str(animSet.infoBlockLengthUncompressed) + ", " +
                                        "got: " + str(len(animSet.infoBlock)) + ") Skipping that set..."))
                continue

            if len(animSet.frameDataBlock) != animSet.frameDataBlockLengthUncompressed:
                logging.warning(warning("Frame data block length in set " + str(setID) + " is incorrect (expected " +
                                        str(animSet.frameDataBlockLengthUncompressed) + ", " +
                                        "got: " + str(len(animSet.frameDataBlock)) + ") Skipping that set..."))
                continue

            if len(animSet.imageDataBlock) != animSet.imageDataBlockLengthUncompressed:
                logging.warning(warning("Image data block length in set " + str(setID) + " is incorrect (expected " +
                                        str(animSet.imageDataBlockLengthUncompressed) + ", " +
                                        "got: " + str(len(animSet.imageDataBlock)) + ") Skipping that set..."))
                continue

            if len(animSet.sampleDataBlock) != animSet.sampleDataBlockLengthUncompressed:
                logging.warning(warning("Sample data block length in set " + str(setID) + " is incorrect (expected " +
                                        str(animSet.sampleDataBlockLengthUncompressed) + ", " +
                                        "got: " + str(len(animSet.sampleDataBlock)) + ") Skipping that set..."))
                continue

            animSet.infoBlock = DataBlock(animSet.infoBlock)
            animSet.frameDataBlock = DataBlock(animSet.frameDataBlock)
            animSet.imageDataBlock = DataBlock(animSet.imageDataBlock)
            animSet.sampleDataBlock = DataBlock(animSet.sampleDataBlock)

            self.sets.append(animSet)

    def __loadAnims(self, setObj):
        for i in range(setObj.animationsCount):
            animSection = Section()

            animSection.ID = i

            animSection.FrameCount = setObj.infoBlock.ReadUShort()
            animSection.FrameRate = setObj.infoBlock.ReadUShort()

            setObj.infoBlock.ReadUInt()  # Seems to be always NULL

            logging.debug(verbose("Set ID: " + str(setObj.ID) + "\t| "
                                  "Anim ID: " + str(i) + "\t| "
                                  "Frame Count: " + str(animSection.FrameCount) + "\t| "
                                  "Frame Rate: " + str(animSection.FrameRate)))

            setObj.anims.append(animSection)

    def __convertAnims(self, setObj):
        if setObj.frameCount > 0:
            if len(setObj.anims) == 0:
                logging.warning(warning("Set " + str(setObj.ID) + " has frames but no anims!"))
                return

        lastColdspotX = 0
        lastColdspotY = 0
        lastHotspotX = 0
        lastHotspotY = 0
        lastGunspotX = 0
        lastGunspotY = 0

        currentAnim = setObj.anims[0]
        currentAnimIdx = 0
        currentFrame = 0

        for i in range(setObj.frameCount):
            if currentFrame >= currentAnim.FrameCount:
                currentAnimIdx += 1
                currentAnim = setObj.anims[currentAnimIdx]
                currentFrame = 0

                while currentAnim.FrameCount == 0 and currentAnimIdx < len(setObj.anims):
                    currentAnimIdx += 1
                    currentAnim = setObj.anims[currentAnimIdx]

            frame = FrameSection()

            frame.SizeX = setObj.frameDataBlock.ReadUShort()
            frame.SizeY = setObj.frameDataBlock.ReadUShort()
            frame.ColdspotX = setObj.frameDataBlock.ReadUShort()
            frame.ColdspotY = setObj.frameDataBlock.ReadUShort()
            frame.HotspotX = setObj.frameDataBlock.ReadUShort()
            frame.HotspotY = setObj.frameDataBlock.ReadUShort()
            frame.GunspotX = setObj.frameDataBlock.ReadUShort()
            frame.GunspotY = setObj.frameDataBlock.ReadUShort()

            frame.ImageAddr = setObj.frameDataBlock.ReadUInt()
            frame.MaskAddr = setObj.frameDataBlock.ReadUInt()

            # Adjust normalized position
            # In the output images, we want to make the hotspot and image size constant
            currentAnim.NormalizedHotspotX = max(-frame.HotspotX, currentAnim.NormalizedHotspotX)
            currentAnim.NormalizedHotspotY = max(-frame.HotspotY, currentAnim.NormalizedHotspotY)

            currentAnim.LargestOffsetX = max(frame.SizeX + frame.HotspotX, currentAnim.LargestOffsetX)
            currentAnim.LargestOffsetY = max(frame.SizeY + frame.HotspotY, currentAnim.LargestOffsetY)

            currentAnim.AdjustedSizeX = max(currentAnim.NormalizedHotspotX + currentAnim.LargestOffsetX,
                                            currentAnim.AdjustedSizeX)
            currentAnim.AdjustedSizeY = max(currentAnim.NormalizedHotspotY + currentAnim.LargestOffsetY,
                                            currentAnim.AdjustedSizeY)

            setObj.anims[currentAnimIdx].Frames.append(frame)

            lastColdspotX = frame.ColdspotX
            lastColdspotY = frame.ColdspotY
            lastHotspotX = frame.HotspotX
            lastHotspotY = frame.HotspotY
            lastGunspotX = frame.GunspotX
            lastGunspotY = frame.GunspotY

            currentFrame += 1

        # Read the image data for each animation frame
        for anim in setObj.anims:
            if anim.FrameCount < len(anim.Frames):
                logging.warning(warning("Animation " + str(anim.ID) + " frame count in set " + str(setObj.ID) +
                                        " doesn't match! Expected " + str(anim.FrameCount) + ", but read " +
                                        str(len(anim.Frames)) + " instead."))
                break

            for frame in anim.Frames:
                dpos = frame.ImageAddr + 4

                setObj.imageDataBlock.context.seek(dpos - 4)
                width = setObj.imageDataBlock.ReadUShort()

                setObj.imageDataBlock.context.seek(dpos - 2)
                height = setObj.imageDataBlock.ReadUShort()

                frame.DrawTransparent = (width & 0x8000) > 0

                pxRead = 0
                pxTotal = frame.SizeX * frame.SizeY
                lastOpEmpty = False

                imageData = []

                while pxRead < pxTotal:
                    if dpos > 0x10000000:
                        logging.warning(warning("Loading of animation " + str(anim.ID) + " in set " + str(setObj.ID) +
                                        "failed!"))
                        break

                    setObj.imageDataBlock.context.seek(dpos)
                    op = setObj.imageDataBlock.ReadByte()

                    if op < 0x80:
                        # Skip the given number of pixels, writing them with the transparent color 0
                        pxRead += op

                        while op > 0:
                            imageData.append(0x00)
                            op -= 1

                        dpos += 1
                    elif op == 0x80:
                        # Skip until the end of the line
                        linePxLeft = frame.SizeX - pxRead % frame.SizeX

                        if pxRead % frame.SizeX == 0 and not lastOpEmpty:
                            linePxLeft = 0

                        pxRead += linePxLeft

                        while linePxLeft > 0:
                            imageData.append(0x00)
                            linePxLeft -= 1

                        dpos += 1
                    else:
                        # Copy specified amount of pixels (ignoring the high bit)
                        bytesToRead = op & 0x7F

                        setObj.imageDataBlock.context.seek(dpos + 1)

                        for byte in range(bytesToRead):
                            imageData.append(setObj.imageDataBlock.ReadByte())

                        pxRead += bytesToRead
                        dpos += bytesToRead + 1

                    lastOpEmpty = op == 0x80

    def save(self, outputPath):
        super().save(outputPath)
