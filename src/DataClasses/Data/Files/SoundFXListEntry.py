from dataclasses import dataclass


@dataclass
class SoundFXListEntry:
    Frame: int = 0
    Sample: int = 0
    Volume: int = 0
    Panning: int = 0
