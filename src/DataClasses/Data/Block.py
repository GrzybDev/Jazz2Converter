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
        t = unpack("I", self.context.read(4))[0]
        return t

    def ReadUShort(self):
        t = unpack("H", self.context.read(2))[0]
        return t

    def ReadByte(self):
        t = unpack("B", self.context.read(1))[0]
        return t
