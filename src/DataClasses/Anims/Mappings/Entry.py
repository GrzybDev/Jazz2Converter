from dataclasses import dataclass


@dataclass
class Entry:
    Category = "UNKNOWN"
    Name = "UNKNOWN"

    Palette = "Std.Palette"
    SkipNormalMap = False
    AddBorder = 0
    AllowRealtimePalette = 0
