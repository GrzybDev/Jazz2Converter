from struct import unpack


class File(object):

    def __init__(self, fileHandle):
        self.context = fileHandle

    def ReadBytes(self, count):
        return self.context.read(count)

    def ReadChar(self):
        return unpack("B", self.context.read(1))[0]

    def ReadUInt(self):
        return unpack("I", self.context.read(4))[0]

    def ReadNullTerminatedString(self):
        jazz2Encoding = "                                 " \
                        "!\"#$% ^()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                        "[\\]∞_`abcdefghijklmnopqrstuvwxyz"\
                        "   ~   ‚ „…    Š Œ             š œ  Ÿ ¡ęóąśłżźćńĘÓĄŚŁŻŹĆŃ           "\
                        "¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"
        temp = ""

        while True:
            char = self.ReadChar()

            if char == 0:
                break

            temp += jazz2Encoding[char]

        return temp
