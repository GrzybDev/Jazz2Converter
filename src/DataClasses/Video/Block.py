class VideoBlock:
    ID = 0
    DataLength = 0
    CompressedLength = 0
    Data = b""

    def __init__(self, _id):
        self.ID = _id
