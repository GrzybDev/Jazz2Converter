import os
import logging
import tempfile
import subprocess
import zlib

from PIL import Image

from src.Helpers.logger import *
from src.Utilities import FileConverter
from src.DataClasses.Video import *
from src.DataClasses.Data import *

class VideoConverter(FileConverter):

    def __init__(self, path):
        super().__init__(path)

        self.FileSize = 0
        self.CRC32 = 0 # Of the lowercase filename

        self.Width = 0
        self.Height = 0

        self.BitsPerPixel = 0
        self.DelayBetweenFrames = 0 # In milliseconds
        self.TotalFrames = 0

        self.CompressedLength = 0

        self.BlocksLength = []
        self.Blocks = []
    
    def convert(self):
        super().convert()

        #try:
        self.__ReadHeader()
        self.__ReadBlocks()

        self.__ExtractFrames()
        #except Exception as e:
        #    logging.error(error("Unexpected error happened during conversion! (" + str(e) + ")")) 

    
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

            logging.debug(verbose(str(self.Width) + "x" + str(self.Height) + " " + str(self.BitsPerPixel) + " bits per pixel. " +
                          str(self.TotalFrames) + " frames. "
                          "Delay between frames: " + str(self.DelayBetweenFrames)))
        else:
            logging.error(error("File has invalid magic string! Expected CineFeed but got: " + magic))
            self.finish()
    
    def __ReadBlocks(self):
        currentPosition = self.file.context.tell()
        self.file.context.seek(0, 2) # Seek to end of the file
        fileLength = self.file.context.tell() # Save file length
        self.file.context.seek(currentPosition) # Revert position

        for i in range(4):
            self.Blocks.append(VideoBlock(i))
        
        while self.file.context.tell() != fileLength:
            for block in self.Blocks:
                block.CompressedLength = self.file.ReadUInt()
                block.Data += self.file.ReadBytes(block.CompressedLength)
                block.DataLength += block.CompressedLength

        for block in self.Blocks:
            if len(block.Data) == block.DataLength:
                decompressor = zlib.decompressobj()
                data = decompressor.decompress(block.Data)
                data += decompressor.flush()
                block.Data = DataBlock(data)
            else:
                logging.error(error("Read " + str(len(block.Data)) + " bytes, but expected " + str(block.CompressedLength)))
                break
    
    def __ExtractFrames(self):
        frame = Image.new("P", [self.Width, self.Height], 255)
        frameID = 0
        palette = []
        self.tempFramesDir = tempfile.TemporaryDirectory()

        for frameID in range(self.TotalFrames):
            pixels = bytearray(frame.tobytes())

            if self.Blocks[0].Data.ReadByte() == 1:
                palette = []

                for color in range(256):
                    palette = palette + [self.Blocks[3].Data.ReadByte(),
                                         self.Blocks[3].Data.ReadByte(),
                                         self.Blocks[3].Data.ReadUShort()]
            
            for y in range(self.Height):
                color = 0
                x = 0

                while (color := self.Blocks[0].Data.ReadByte()) != 128:
                    if color < 128:
                        u = self.Blocks[0].Data.ReadUShort() if color == 0 else color

                        for i in range(u):
                            pixels[y * self.Width + x] = self.Blocks[3].Data.ReadByte()
                            x += 1
                    else:
                        u = self.Blocks[0].Data.ReadUShort() if color == 0x81 else color - 106
                        n = self.Blocks[1].Data.ReadUShort() + (self.Blocks[2].Data.ReadByte() + y - 127) * self.Width

                        for i in range(u):
                            pixels[y * self.Width + x] = pixels[n]
                            n += 1
                            x += 1

            frame = Image.frombytes(frame.mode, (frame.width, frame.height), bytes(pixels))
            frame.putpalette(palette)
            frame.save(self.tempFramesDir.name + "/" + str(frameID) + ".bmp")
    
    def save(self, outputPath):
        super().save(outputPath)

        try:
            logging.info("Now optimizing video file using FFMpeg...")
            subprocess.call(["ffmpeg",
                             "-f", "image2",
                             "-r", str(self.DelayBetweenFrames),
                             "-i", self.tempFramesDir.name + "/%d.bmp",
                             "-pix_fmt", "yuv420p",
                             outputPath + os.path.splitext(os.path.basename(self.path))[0] + ".mp4"])
        except FileNotFoundError:
            logging.error(error("FFMpeg is not accessible, please install it system-wise or place it in current folder!"))
        except Exception as e:
            logging.error(error("Unexpected error happened during optimization! (" + str(e) + ")"))
