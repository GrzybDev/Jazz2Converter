import zlib
from io import BytesIO
from struct import unpack

from src.Logger import error


class DataBlock:
    def __init__(self, data, dataLength, uncompressedLength=0):
        if uncompressedLength == 0:
            self.context = BytesIO(data)
        else:
            if len(data) != dataLength:
                error("Invalid DataBlock length! "
                      "(Expected " + str(dataLength) + " bytes, but got: " + str(len(data)) + " bytes)!")
                raise ValueError("Invalid DataBlock length!")

            dec = zlib.decompress(data)

            if len(dec) != uncompressedLength:
                error("Invalid decompressed datablock length! "
                      "(Expected " + str(uncompressedLength) + " bytes, but got: " + str(len(dec)) + "bytes)!")
                raise ValueError("Invalid decompressed DataBlock length!")

            self.context = BytesIO(dec)

    def DiscardBytes(self, count):
        self.context.read(count)

    def ReadBool(self):
        return unpack("?", self.context.read(1))[0]

    def ReadByte(self):
        return unpack("B", self.context.read(1))[0]

    def ReadEncodedFloat(self):
        return unpack("i", self.context.read(4))[0] * 1.0 / 65536

    def ReadRawBytes(self, count, fromOffset=None):
        if fromOffset is not None:
            self.context.seek(fromOffset)

        bytesArray = []

        for byte in range(count):
            bytesArray.append(self.ReadByte())

        return bytesArray

    def ReadShort(self):
        return unpack("h", self.context.read(2))[0]

    def ReadString(self, length, trimToNull=False):
        result = self.context.read(length)

        if trimToNull:
            result = result.split(b"\x00")[0]

        return result.decode()

    def ReadUInt(self):
        return unpack("I", self.context.read(4))[0]

    def ReadUShort(self):
        return unpack("H", self.context.read(2))[0]
