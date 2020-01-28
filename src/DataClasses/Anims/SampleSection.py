from dataclasses import dataclass


@dataclass
class SampleSection:
    SampleRate = 0
    Data = []
    Multiplier = 0

    TotalSize = 0
    ChunkSize = 0
    Format = 0
    IsASFF = False
    SampleSize = 0
    PayloadSize = 0
    ActualDataSize = 0
