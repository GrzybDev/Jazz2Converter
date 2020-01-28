from dataclasses import dataclass


@dataclass
class DataFile:
    Name: str = ""

    Type: int = 0
    Offset: int = 0

    FileCRC: int = 0

    FilePackedSize: int = 0
    FileUnpackedSize: int = 0
