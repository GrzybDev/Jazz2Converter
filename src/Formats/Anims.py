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

        self.anims = []
        self.samples = []

    def convert(self):
        super().convert()

        try:
            self.__checkFile()
            self.__loadHeader()

            self.__loadSets()
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

            anims = []

            if magic != 0x4D494E41:
                logging.warning(warning("Header for set " + str(setID) + " is incorrect (bad magic value!) "
                                        "Skipping that set..."))
                continue

            for animID in range(animSet.animationsCount):
                anim = Section()

                anim.ID = animID

                anim.FrameCount = animSet.infoBlock.ReadUShort()
                anim.FrameRate = animSet.infoBlock.ReadUShort()
                anim.Frames = [FrameSection()] * anim.FrameCount

                animSet.infoBlock.DiscardBytes(4)  # Skip 4 bytes, seems to be NULL in every set

                logging.debug(verbose("Set ID: " + str(animSet.ID) + "\t| "
                                      "Anim ID: " + str(anim.ID) + "\t| "
                                      "Frame Count: " + str(anim.FrameCount) + "\t| "
                                      "Frame Rate: " + str(anim.FrameRate)))

                self.anims.append(anim)
                anims.append(anim)

            if animSet.frameCount > 0:
                if len(animSet.anims) == 0:
                    logging.error(error("Set has frames, but no animations... File is corrupted!"))
                    raise ValueError("Set has frames but no animations")

                currentAnim = animSet.anims[0]
                currentAnimID, currentFrame = (0, 0)

                for frameID in range(animSet.frameCount):
                    if currentFrame >= currentAnim.FrameCount:
                        currentAnimID += 1

                        currentAnim = animSet.anims[currentAnimID]
                        currentFrame = 0

                        while currentAnim.FrameCount == 0 and currentAnimID < len(animSet.anims):
                            currentAnimID += 1
                            currentAnim = animSet.anims[currentAnimID]

                    frame = currentAnim.Frames[currentFrame]

                    frame.SizeX, frame.SizeY = (animSet.frameDataBlock.ReadUShort(),
                                                animSet.frameDataBlock.ReadUShort())

                    frame.ColdspotX, frame.ColdspotY = (animSet.frameDataBlock.ReadUShort(),
                                                        animSet.frameDataBlock.ReadUShort())

                    frame.HotspotX, frame.HotspotY = (animSet.frameDataBlock.ReadUShort(),
                                                      animSet.frameDataBlock.ReadUShort())

                    frame.GunspotX, frame.GunspotY = (animSet.frameDataBlock.ReadUShort(),
                                                      animSet.frameDataBlock.ReadUShort())

                    frame.ImageAddr, frame.MaskAddr = (animSet.frameDataBlock.ReadUInt(),
                                                       animSet.frameDataBlock.ReadUInt())

                    # Adjust normalized position
                    # In the output images, we want to make the hotspot and image size constant.
                    currentAnim.NormalizedHotspotX = max(-frame.HotspotX, currentAnim.NormalizedHotspotX)
                    currentAnim.NormalizedHotspotY = max(-frame.HotspotY, currentAnim.NormalizedHotspotY)

                    currentAnim.LargestOffsetX = max(frame.SizeX + frame.HotspotX, currentAnim.LargestOffsetX)
                    currentAnim.LargestOffsetY = max(frame.SizeY + frame.HotspotY, currentAnim.LargestOffsetY)

                    currentAnim.AdjustedSizeX = max(currentAnim.NormalizedHotspotX + currentAnim.LargestOffsetX,
                                                    currentAnim.AdjustedSizeX)
                    currentAnim.AdjustedSizeY = max(currentAnim.NormalizedHotspotY + currentAnim.LargestOffsetY,
                                                    currentAnim.AdjustedSizeY)

                    currentFrame += 1

                # Read the image data for each animation frame
                for animID in range(animSet.animationsCount):
                    anim = animSet.anims[animID]

                    if anim.FrameCount != len(anim.Frames):
                        logging.error(warning("Animation " + str(anim.ID) + " frame count in set " +
                                              str(animSet.ID) + " doesn't match! (Expected " +
                                              str(anim.FrameCount) + " frames, but read " +
                                              str(len(anim.Frames)) + " instead.)"))
                        raise ValueError("Animation count mismatch")

                    for frame in range(anim.FrameCount):
                        dpos = anim.Frames[frame].ImageAddr + 4

                        animSet.imageDataBlock.context.seek(dpos - 4)
                        width = animSet.imageDataBlock.ReadUShort()

                        animSet.imageDataBlock.context.seek(dpos - 2)
                        height = animSet.imageDataBlock.ReadUShort()

                        frameData = anim.Frames[frame]
                        frameData.DrawTransparent = (width & 0x8000) > 0

                        pxRead = 0
                        pxTotal = frameData.SizeX * frameData.SizeY
                        lastOpEmpty = True

                        imageData = []

                        while pxRead < pxTotal:
                            if dpos > 0x10000000:
                                logging.warning("Loading of animation " + str(anim.ID) + " in set " +
                                                str(animSet.ID) + " failed! Aborting...")
                                break

                            animSet.imageDataBlock.context.seek(dpos)

                            op = animSet.imageDataBlock.ReadByte()

                            if op < 0x80:
                                # Skip the given number of pixels, writing them with transparent color 0
                                pxRead += op

                                while op > 0:
                                    op -= 1
                                    imageData.append(0x00)

                                dpos += 1
                            elif op == 0x80:
                                # Skip until the end of the line
                                linePxLeft = frameData.SizeX - pxRead % frameData.SizeX

                                if pxRead % frameData.SizeX == 0 and not lastOpEmpty:
                                    linePxLeft = 0

                                pxRead += linePxLeft

                                while linePxLeft > 0:
                                    linePxLeft -= 1
                                    imageData.append(0x00)

                                dpos += 1
                            else:
                                # Copy specified amount of pixels (ignoring the high bit)
                                bytesToRead = op & 0x7F

                                animSet.imageDataBlock.context.seek(dpos + 1)
                                nextData = animSet.imageDataBlock.ReadRawBytes(bytesToRead)
                                imageData = imageData + nextData

                                pxRead += bytesToRead
                                dpos += bytesToRead + 1

                            lastOpEmpty = op == 0x80

                        frameData.ImageData = imageData
                        frameData.MaskData = [False] * pxTotal

                        dpos = frameData.MaskAddr
                        pxRead = 0

                        if dpos == 0xFFFFFFFF:  # No mask
                            continue

                        while pxRead < pxTotal:
                            animSet.imageDataBlock.context.seek(dpos)
                            byte = animSet.imageDataBlock.ReadByte()

                            bit = 0
                            while bit < 8 and (pxRead + bit) < pxTotal:
                                frameData.MaskData[(pxRead + bit)] = (byte & (1 << (7 - bit))) != 0
                                bit += 1

                            pxRead += 8

            for soundID in range(animSet.soundsCount):
                sample = SampleSection()
                sample.IdInSet = soundID

                sample.totalSize = animSet.sampleDataBlock.ReadUInt()
                magicRIFF = animSet.sampleDataBlock.ReadUInt()

                sample.chunkSize = animSet.sampleDataBlock.ReadUInt()
                sample.Format = animSet.sampleDataBlock.ReadUInt() # "ASFF" for 1.20, "AS  " for 1.24
                sample.isASFF = sample.Format == 0x46465341

                magicSAMP = animSet.sampleDataBlock.ReadUInt()
                sample.sampSize = animSet.sampleDataBlock.ReadUInt()

                # Skip unknown data
                animSet.sampleDataBlock.DiscardBytes(40 - (12 if sample.isASFF else 0))

                if sample.isASFF:
                    # All 1.20 samples seem to be 8-bit. Some of them are among those
                    # for which 1.24 reads as 24-bit but that might just be a mistake.
                    animSet.sampleDataBlock.DiscardBytes(2)
                    sample.Multiplier = 0
                else:
                    # for 1.24. 1.20 has "20 40" instead in s0s0 which makes no sense
                    sample.Multiplier = animSet.sampleDataBlock.ReadUShort()

                # Unknown. s0s0 1.20: 00 80, 1.24: 80 00
                animSet.sampleDataBlock.DiscardBytes(2)

                sample.payloadSize = animSet.sampleDataBlock.ReadUInt()

                # Padding #2, all zeroes in both
                animSet.sampleDataBlock.DiscardBytes(8)

                sample.SampleRate = animSet.sampleDataBlock.ReadUInt()
                sample.actualDataSize = sample.chunkSize - 76 + (12 if sample.isASFF else 0)

                sample.Data = animSet.sampleDataBlock.ReadRawBytes(sample.actualDataSize)

                # Padding #3
                animSet.sampleDataBlock.DiscardBytes(4)

                if magicRIFF != 0x46464952 or magicSAMP != 0x504D4153:
                    logging.error(error("Sample has invalid header"))
                    raise ValueError("Sample has invalid header")

                if len(sample.Data) < sample.actualDataSize:
                    logging.warning(warning("Sample " + str(sample.IdInSet) + " in set " + str(animSet.ID) + " was "
                                            "shorter than expected! Expected " + str(sample.actualDataSize) + " bytes, "
                                            "but read " + str(len(sample.Data)) + " instead."))

                if sample.totalSize > sample.chunkSize + 12:
                    # Sample data is probably aligned to X bytes since the next sample doesn't always appear right after the first ends.
                    logging.warning(warning("Adjusting read offset of sample " + str(sample.IdInSet) + " in set " +
                                            str(animSet.ID) + " by " + str(sample.totalSize - sample.chunkSize - 12) +
                                            " bytes."))

                    animSet.sampleDataBlock.DiscardBytes(sample.totalSize - sample.chunkSize - 12)

                animSet.samples.append(sample)

    def save(self, outputPath):
        super().save(outputPath)
