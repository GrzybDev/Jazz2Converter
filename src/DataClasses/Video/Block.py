from dataclasses import dataclass


@dataclass
class VideoBlock:
    ID: int = 0
    DataLength = 0
    CompressedLength = 0
    Data = b""
