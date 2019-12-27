from struct import unpack


class File(object):

    def __init__(self, fileHandle):
        self.context = fileHandle

    def ReadBytes(self, count):
        return self.context.read(count)

    def ReadByte(self):
        return unpack("B", self.context.read(1))[0]

    def ReadUInt(self):
        return unpack("I", self.context.read(4))[0]
