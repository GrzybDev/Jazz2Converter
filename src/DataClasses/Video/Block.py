from dataclasses import dataclass


@dataclass
class VideoBlock:
    ID: int = 0
    CompressedLength = 0
    CompressedData = b""
    CompressedDataLength = 0
    Data = None
