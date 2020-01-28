from dataclasses import dataclass


@dataclass
class FrameSection:
    SizeX, SizeY = (0, 0)
    ColdspotX, ColdspotY = (0, 0)
    HotspotX, HotspotY = (0, 0)
    GunspotX, GunspotY = (0, 0)

    ImageAddr, MaskAddr = (0, 0)

    DrawTransparent = False

    ImageData, MaskData = ([], [])
