import logging
import math
import zlib

from pathlib import Path
from PIL import Image
from struct import pack

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
            magic = self.file.ReadUInt()

            animationsCount = self.file.ReadByte()
            soundsCount = self.file.ReadByte()
            frameCount = self.file.ReadUShort()
            cumulativeSoundIndex = self.file.ReadUInt()

            infoBlockLengthCompressed = self.file.ReadUInt()
            infoBlockLengthUncompressed = self.file.ReadUInt()
            frameDataBlockLengthCompressed = self.file.ReadUInt()
            frameDataBlockLengthUncompressed = self.file.ReadUInt()
            imageDataBlockLengthCompressed = self.file.ReadUInt()
            imageDataBlockLengthUncompressed = self.file.ReadUInt()
            sampleDataBlockLengthCompressed = self.file.ReadUInt()
            sampleDataBlockLengthUncompressed = self.file.ReadUInt()

            infoBlock = self.file.ReadBytes(infoBlockLengthCompressed)
            frameDataBlock = self.file.ReadBytes(frameDataBlockLengthCompressed)
            imageDataBlock = self.file.ReadBytes(imageDataBlockLengthCompressed)
            sampleDataBlock = self.file.ReadBytes(sampleDataBlockLengthCompressed)

            infoBlock = zlib.decompress(infoBlock)
            frameDataBlock = zlib.decompress(frameDataBlock)
            imageDataBlock = zlib.decompress(imageDataBlock)
            sampleDataBlock = zlib.decompress(sampleDataBlock)

            if len(infoBlock) != infoBlockLengthUncompressed:
                logging.warning(warning("Info block length in set " + str(setID) + " is incorrect (expected " +
                                        str(infoBlockLengthUncompressed) + ", " +
                                        "got: " + str(len(infoBlock)) + ") Skipping that set..."))
                continue

            if len(frameDataBlock) != frameDataBlockLengthUncompressed:
                logging.warning(warning("Frame data block length in set " + str(setID) + " is incorrect (expected " +
                                        str(frameDataBlockLengthUncompressed) + ", " +
                                        "got: " + str(len(frameDataBlock)) + ") Skipping that set..."))
                continue

            if len(imageDataBlock) != imageDataBlockLengthUncompressed:
                logging.warning(warning("Image data block length in set " + str(setID) + " is incorrect (expected " +
                                        str(imageDataBlockLengthUncompressed) + ", " +
                                        "got: " + str(len(imageDataBlock)) + ") Skipping that set..."))
                continue

            if len(sampleDataBlock) != sampleDataBlockLengthUncompressed:
                logging.warning(warning("Sample data block length in set " + str(setID) + " is incorrect (expected " +
                                        str(sampleDataBlockLengthUncompressed) + ", " +
                                        "got: " + str(len(sampleDataBlock)) + ") Skipping that set..."))
                continue

            infoBlock = DataBlock(infoBlock)
            frameDataBlock = DataBlock(frameDataBlock)
            imageDataBlock = DataBlock(imageDataBlock)
            sampleDataBlock = DataBlock(sampleDataBlock)

            anims = []

            if magic != 0x4D494E41:
                logging.warning(warning("Header for set " + str(setID) + " is incorrect (bad magic value!) "
                                        "Skipping that set..."))
                continue

            for animID in range(animationsCount):
                anim = Section()

                anim.Set = setID
                anim.Anim = animID
                anim.FrameCount = infoBlock.ReadUShort()
                anim.FrameRate = infoBlock.ReadUShort()
                anim.Frames = []

                infoBlock.DiscardBytes(4)  # Skip 4 bytes, seems to be NULL in every set

                logging.debug(verbose("Set ID: " + str(setID) + "\t| "
                                      "Anim ID: " + str(animID) + "\t| "
                                      "Frame Count: " + str(anim.FrameCount) + "\t| "
                                      "Frame Rate: " + str(anim.FrameRate)))

                self.anims.append(anim)
                anims.append(anim)

            if frameCount > 0:
                if len(anims) == 0:
                    logging.error(error("Set has frames, but no animations... File is corrupted!"))
                    raise ValueError("Set has frames but no animations")

                currentAnim = anims[0]
                currentAnimID, currentFrame = (0, 0)

                for frameID in range(frameCount):
                    if currentFrame >= currentAnim.FrameCount:
                        currentAnimID += 1

                        currentAnim = anims[currentAnimID]
                        currentFrame = 0

                        while currentAnim.FrameCount == 0 and currentAnimID < len(anims):
                            currentAnimID += 1
                            currentAnim = anims[currentAnimID]

                    frame = FrameSection()

                    frame.SizeX, frame.SizeY = (frameDataBlock.ReadUShort(),
                                                frameDataBlock.ReadUShort())

                    frame.ColdspotX, frame.ColdspotY = (frameDataBlock.ReadShort(),
                                                        frameDataBlock.ReadShort())

                    frame.HotspotX, frame.HotspotY = (frameDataBlock.ReadShort(),
                                                      frameDataBlock.ReadShort())

                    frame.GunspotX, frame.GunspotY = (frameDataBlock.ReadShort(),
                                                      frameDataBlock.ReadShort())

                    frame.ImageAddr, frame.MaskAddr = (frameDataBlock.ReadUInt(),
                                                       frameDataBlock.ReadUInt())

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
                    currentAnim.Frames.append(frame)

                # Read the image data for each animation frame
                for animID in range(animationsCount):
                    anim = anims[animID]

                    if anim.FrameCount != len(anim.Frames):
                        logging.error(warning("Animation " + str(animID) + " frame count in set " +
                                              str(setID) + " doesn't match! (Expected " +
                                              str(anim.FrameCount) + " frames, but read " +
                                              str(len(anim.Frames)) + " instead.)"))
                        raise ValueError("Animation count mismatch")

                    for frame in range(anim.FrameCount):
                        dpos = anim.Frames[frame].ImageAddr + 4

                        imageDataBlock.context.seek(dpos - 4)
                        width = imageDataBlock.ReadUShort()

                        imageDataBlock.context.seek(dpos - 2)
                        height = imageDataBlock.ReadUShort()

                        frameData = anim.Frames[frame]
                        frameData.DrawTransparent = (width & 0x8000) > 0

                        pxRead = 0
                        pxTotal = frameData.SizeX * frameData.SizeY
                        lastOpEmpty = True

                        imageData = []

                        while pxRead < pxTotal:
                            if dpos > 0x10000000:
                                logging.warning("Loading of animation " + str(animID) + " in set " +
                                                str(setID) + " failed! Aborting...")
                                break

                            imageDataBlock.context.seek(dpos)

                            op = imageDataBlock.ReadByte()

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

                                imageDataBlock.context.seek(dpos + 1)
                                nextData = imageDataBlock.ReadRawBytes(bytesToRead)
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
                            imageDataBlock.context.seek(dpos)
                            byte = imageDataBlock.ReadByte()

                            bit = 0
                            while bit < 8 and (pxRead + bit) < pxTotal:
                                frameData.MaskData[(pxRead + bit)] = (byte & (1 << (7 - bit))) != 0
                                bit += 1

                            pxRead += 8

            for soundID in range(soundsCount):
                sample = SampleSection()

                sample.Set = setID
                sample.IdInSet = soundID

                sample.totalSize = sampleDataBlock.ReadUInt()
                magicRIFF = sampleDataBlock.ReadUInt()

                sample.chunkSize = sampleDataBlock.ReadUInt()
                sample.Format = sampleDataBlock.ReadUInt() # "ASFF" for 1.20, "AS  " for 1.24
                sample.isASFF = sample.Format == 0x46465341

                magicSAMP = sampleDataBlock.ReadUInt()
                sample.sampSize = sampleDataBlock.ReadUInt()

                # Skip unknown data
                sampleDataBlock.DiscardBytes(40 - (12 if sample.isASFF else 0))

                if sample.isASFF:
                    # All 1.20 samples seem to be 8-bit. Some of them are among those
                    # for which 1.24 reads as 24-bit but that might just be a mistake.
                    sampleDataBlock.DiscardBytes(2)
                    sample.Multiplier = 0
                else:
                    # for 1.24. 1.20 has "20 40" instead in s0s0 which makes no sense
                    sample.Multiplier = sampleDataBlock.ReadUShort()

                # Unknown. s0s0 1.20: 00 80, 1.24: 80 00
                sampleDataBlock.DiscardBytes(2)

                sample.payloadSize = sampleDataBlock.ReadUInt()

                # Padding #2, all zeroes in both
                sampleDataBlock.DiscardBytes(8)

                sample.SampleRate = sampleDataBlock.ReadUInt()
                sample.actualDataSize = sample.chunkSize - 76 + (12 if sample.isASFF else 0)

                sample.Data = sampleDataBlock.ReadRawBytes(sample.actualDataSize)

                # Padding #3
                sampleDataBlock.DiscardBytes(4)

                if magicRIFF != 0x46464952 or magicSAMP != 0x504D4153:
                    logging.error(error("Sample has invalid header"))
                    raise ValueError("Sample has invalid header")

                if len(sample.Data) < sample.actualDataSize:
                    logging.warning(warning("Sample " + str(soundID) + " in set " + str(setID) + " was "
                                            "shorter than expected! Expected " + str(sample.actualDataSize) + " bytes, "
                                            "but read " + str(len(sample.Data)) + " instead."))

                if sample.totalSize > sample.chunkSize + 12:
                    # Sample data is probably aligned to X bytes since the next sample doesn't always appear right
                    # after the first ends.
                    logging.warning(warning("Adjusting read offset of sample " + str(soundID) + " in set " +
                                            str(setID) + " by " + str(sample.totalSize - sample.chunkSize - 12) +
                                            " bytes."))

                    sampleDataBlock.DiscardBytes(sample.totalSize - sample.chunkSize - 12)

                self.samples.append(sample)

    def __extractAnimations(self, path):
        if len(self.anims) > 0:
            logging.info(info("Now extracting animations..."))

            for anim in self.anims:
                if anim.FrameCount == 0:
                    continue

                sizeX, sizeY = (anim.AdjustedSizeX, anim.AdjustedSizeY)

                if anim.FrameCount > 1:
                    rows = max(1, math.ceil(math.sqrt(anim.FrameCount * sizeX / sizeY)))
                    columns = max(1, math.ceil(anim.FrameCount / rows))

                    while columns * (rows - 1) >= anim.FrameCount:
                        rows -= 1

                    anim.FrameConfigurationX, anim.FrameConfigurationY = (columns, rows)
                else:
                    anim.FrameConfigurationX, anim.FrameConfigurationY = (anim.FrameCount, 1)

                image = Image.new("RGBA", [sizeX, sizeY], 255)
                imageData = image.load()

                for frameID in range(len(anim.Frames)):
                    frame = anim.Frames[frameID]

                    offsetX, offsetY = (anim.NormalizedHotspotX + frame.HotspotX,
                                        anim.NormalizedHotspotY + frame.HotspotY)

                    for y in range(frame.SizeY):
                        for x in range(frame.SizeX):
                            targetX, targetY = (int((frameID % anim.FrameConfigurationX) * sizeX + offsetX + x),
                                                int((frameID / anim.FrameConfigurationX) * sizeY + offsetY + y))

                            colorID = frame.ImageData[frame.SizeX * y + x]

                            alpha = 255

                            if frame.DrawTransparent:
                                alpha = min(140, alpha)

                            try:  # TODO: Fix that
                                imageData[targetX, targetY] = (colorID, colorID, colorID, alpha)
                            except IndexError:
                                continue

                Path(path + "/" + str(anim.Set)).mkdir(exist_ok=True)
                image.save(path + "/" + str(anim.Set) + "/" + str(anim.Anim) + ".png")

    def __extractAudioSamples(self, path):
        if len(self.samples) > 0:
            logging.info(info("Now extracting audio samples..."))

            for sample in self.samples:
                Path(path + "/" + str(sample.Set)).mkdir(exist_ok=True)

                with open(path + "/" + str(sample.Set) + "/" + str(sample.IdInSet) + ".wav", "wb") as sampleFile:
                    multiplier = int((sample.Multiplier / 4) % 2 + 1)

                    # Create PCM Wave File
                    # Main header
                    sampleFile.write(b"RIFF")
                    sampleFile.write(pack("I", 36 + len(sample.Data)))  # File size
                    sampleFile.write(b"WAVE")

                    # Format header
                    sampleFile.write(b"fmt ")
                    sampleFile.write(pack("I", 16))  # Remaining header length
                    sampleFile.write(pack("H", 1))  # Format == PCM
                    sampleFile.write(pack("H", 1))  # Channels
                    sampleFile.write(pack("I", sample.SampleRate))  # Sample Rate
                    sampleFile.write(pack("I", sample.SampleRate * multiplier))  # Bytes per second
                    sampleFile.write(pack("I", multiplier * 0x00080001))

                    # Payload
                    sampleFile.write(b"data")
                    sampleFile.write(pack("I", len(sample.Data)))  # Payload length

                    for byte in sample.Data:
                        try:  # TODO: Fix 256-byte error
                            sampleFile.write(pack("B", (multiplier << 7) ^ byte))
                        except Exception:
                            continue

                    sampleFile.close()

    def save(self, outputPath):
        super().save(outputPath)

        self.__extractAnimations(outputPath)
        self.__extractAudioSamples(outputPath)
