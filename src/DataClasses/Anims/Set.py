class Set:
    ID = 0

    animationsCount = 0
    soundsCount = 0
    frameCount = 0
    cumulativeSoundIndex = 0

    infoBlockLengthCompressed = 0
    infoBlockLengthUncompressed = 0
    frameDataBlockLengthCompressed = 0
    frameDataBlockLengthUncompressed = 0
    imageDataBlockLengthCompressed = 0
    imageDataBlockLengthUncompressed = 0
    sampleDataBlockLengthCompressed = 0
    sampleDataBlockLengthUncompressed = 0

    infoBlock = None
    frameDataBlock = None
    imageDataBlock = None
    sampleDataBlock = None

    anims = []
