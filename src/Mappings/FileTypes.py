from src.Formats.DataAssets import *

fileTypes = {
    0x23: PictureDataFile,
    0x18: PictureDataFile,
    0x1D: PictureDataFile,
    0x17: PictureDataFile,
    0x16: PictureDataFile,
    0x19: PictureDataFile,
    0x1A: PictureDataFile,
    0x15: PictureDataFile,
    0x52: PictureDataFile,
    0x9: PaletteDataFile,
    0xFFFFFFFF: PaletteDataFile,
    0x11C9A10: SoundFXList,
    0x11C8330: SoundFXList,
    0x11C88A0: SoundFXList,
    0x11C8750: SoundFXList,
    0x11C8320: SoundFXList,
    0x11C8AB0: TextureDataFile
}