from dataclasses import dataclass


@dataclass
class LayerSection:
    Flags = 0
    Type = 0
    Used = False

    Width = 0
    InternalWidth = 0
    Height = 0
    Depth = 0

    DetailLevel = 0

    WaveX, WaveY = (0, 0)
    SpeedX, SpeedY = (0, 0)
    AutoSpeedX, AutoSpeedY = (0, 0)

    TexturedBackgroundType = 0
    TexturedParams1, TexturedParams2, TexturedParams3 = (0, 0, 0)

    Tiles = []
