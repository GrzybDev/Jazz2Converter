from dataclasses import dataclass


@dataclass
class TileSection:
    Opaque = False
    ImageDataOffset = 0
    AlphaDataOffset = 0
    MaskDataOffset = 0

    Image = None
    Mask = None
