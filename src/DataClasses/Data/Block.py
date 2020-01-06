from io import BytesIO

from struct import unpack


class DataBlock:

    def __init__(self, data):
        self.context = BytesIO(data)

    def ReadString(self, length, trimToNull=False):
        result = self.context.read(length)

        if trimToNull:
            result = result.split(b"\x00")[0]

        return result.decode()
    
    def ReadUInt(self):
        return unpack("I", self.context.read(4))[0]

    def ReadShort(self):
        return unpack("h", self.context.read(2))[0]

    def ReadUShort(self):
        return unpack("H", self.context.read(2))[0]

    def ReadByte(self):
        return unpack("B", self.context.read(1))[0]

    def ReadRawBytes(self, count):
        bytesArray = []

        for byte in range(count):
            bytesArray.append(self.ReadByte())

        return bytesArray

    def DiscardBytes(self, count):
        self.context.read(count)
