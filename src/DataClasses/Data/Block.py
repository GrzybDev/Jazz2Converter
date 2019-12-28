from struct import unpack


class DataBlock:

    def __init__(self, data):
        self.data = data

    def ReadString(self, length, trimToNull=False):
        result = self.data[:length]

        if trimToNull:
            result = result.split(b"\x00")[0]
        
        self.data = self.data[length:]
        return result.decode()
    
    def ReadUInt(self):
        result = unpack("I", self.data[:4])
        self.data = self.data[4:]

        return result[0]
