from dataclasses import dataclass


@dataclass
class Section:
    FrameCount = 0
    FrameRate = 0
    Frames = []

    NormalizedHotspotX, NormalizedHotspotY = (0, 0)
    LargestOffsetX, LargestOffsetY = (0, 0)
    AdjustedSizeX, AdjustedSizeY = (0, 0)
    FrameConfigurationX, FrameConfigurationY = (0, 0)
