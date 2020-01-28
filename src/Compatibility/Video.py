import os
import subprocess
import tempfile
import zlib

from PIL import Image

from src.DataClasses.Video.Block import VideoBlock
from src.Logger import verbose, error, info
from src.Utilities.DataBlock import DataBlock
from src.Utilities.FileConverter import FileConverter


class VideoConverter(FileConverter):
    def __init__(self, path):
        super().__init__(path)

        self.FileSize = 0
        self.CRC32 = 0  # Of the lowercase filename

        self.Width = 0
        self.Height = 0

        self.BitsPerPixel = 0
        self.DelayBetweenFrames = 0  # In milliseconds
        self.TotalFrames = 0

        self.CompressedLength = 0

        self.BlocksLength = []
        self.Blocks = []

    def _FileConverter__convert(self):
        self.__ReadHeader()
        self.__ReadBlocks()

        self.__ExtractFrames()

    def __ReadHeader(self):
        magic = self.file.ReadString(8).decode()

        if magic == "CineFeed":
            self.FileSize = self.file.ReadUInt()
            self.CRC32 = self.file.ReadUInt()
            self.Width = self.file.ReadUInt()
            self.Height = self.file.ReadUInt()
            self.BitsPerPixel = self.file.ReadUShort()
            self.DelayBetweenFrames = self.file.ReadUShort()
            self.TotalFrames = self.file.ReadUInt()

            for i in range(4):
                self.BlocksLength.append(self.file.ReadUInt())

            self.CompressedLength = self.file.ReadUInt()

            verbose(str(self.Width) + "x" + str(self.Height) + " " + str(self.BitsPerPixel) + " bits per pixel. " +
                    str(self.TotalFrames) + " frames. Delay between frames: " + str(self.DelayBetweenFrames))
        else:
            error("File has invalid magic string! Expected CineFeed but got: " + magic)
            raise ValueError("Invalid magic number!")

    def __ReadBlocks(self):
        currentPosition = self.file.context.tell()
        self.file.context.seek(0, 2)  # Seek to end of the file
        fileLength = self.file.context.tell()  # Save file length
        self.file.context.seek(currentPosition)  # Revert position

        for i in range(4):
            self.Blocks.append(VideoBlock(i))

        rawData = ""
        while self.file.context.tell() != fileLength:
            for block in self.Blocks:
                block.CompressedLength = self.file.ReadUInt()
                rawData += self.file.ReadBytes(block.CompressedLength)
                block.DataLength += block.CompressedLength

        for block in self.Blocks:
            if len(rawData) == block.DataLength:
                decompressor = zlib.decompressobj()
                data = decompressor.decompress(rawData)
                data += decompressor.flush()
                block.Data = DataBlock(data, len(data))
            else:
                error("Read " + str(len(rawData)) + " bytes, but expected " + str(block.CompressedLength))
                break

    def __ExtractFrames(self):
        frame = Image.new("P", [self.Width, self.Height], 0)
        palette = []
        self.tempFramesDir = tempfile.TemporaryDirectory()

        for frameID in range(self.TotalFrames):
            pixels = bytearray(frame.tobytes())
            copy = []

            for x in range(self.Width * self.Height):
                copy.append(pixels[x])

            if self.Blocks[0].Data.ReadByte() == 1:
                palette = []

                for c in range(256):
                    palette = palette + [
                        self.Blocks[3].Data.ReadByte(),
                        self.Blocks[3].Data.ReadByte(),
                        self.Blocks[3].Data.ReadUShort(),
                    ]

            for y in range(self.Height):
                c = self.Blocks[0].Data.ReadByte()
                x = 0

                while c != 128:
                    if c < 128:
                        u = self.Blocks[0].Data.ReadUShort() if c == 0 else c

                        for i in range(u):
                            pixels[(y * self.Width) + x] = self.Blocks[
                                3
                            ].Data.ReadByte()
                            x += 1
                    else:
                        u = self.Blocks[0].Data.ReadUShort() if c == 0x81 else c - 106
                        n = (
                                self.Blocks[1].Data.ReadUShort()
                                + (self.Blocks[2].Data.ReadByte() + y - 127) * self.Width
                        )

                        for i in range(u):
                            pixels[(y * self.Width) + x] = copy[n]
                            x += 1
                            n += 1

            frame = Image.frombytes(
                frame.mode, (frame.width, frame.height), bytes(pixels)
            )
            frame.putpalette(palette)
            frame.save(self.tempFramesDir.name + "/" + str(frameID) + ".bmp")

    def _FileConverter__save(self, outputPath):
        defaultDuration = self.TotalFrames / 25
        correctDuration = self.DelayBetweenFrames * self.TotalFrames / 1000
        correction = 1 + (correctDuration - defaultDuration) / defaultDuration

        info("Now optimizing video file using FFMpeg...")
        subprocess.call(
            [
                "ffmpeg",
                "-i",
                self.tempFramesDir.name + "/%d.bmp",
                "-pix_fmt",
                "yuv420p",
                "-filter:v",
                "setpts=" + str(correction) + "*PTS,fps=60",
                outputPath
                + os.path.splitext(os.path.basename(self.path))[0]
                + ".mp4",
            ]
        )
