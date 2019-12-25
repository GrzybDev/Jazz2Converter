from struct import unpack


class File(object):

    def __init__(self, fileHandle):
        self.context = fileHandle

    def ReadBytes(self, count):
        return self.context.read(count)

    def ReadUInt(self):
        return unpack("I", self.context.read(4))[0]

    def ReadNullTerminatedString(self):
        temp = ""

        while True:
            char = self.context.read(1)

            if char == b'\x00':
                break
            elif char == b'\x5c':
                temp += '\\'
                continue

            # TODO: Convert Jazz Jackrabbit 2 Encoded text to Unicode

            temp += char.decode('unicode_escape')

        return temp
