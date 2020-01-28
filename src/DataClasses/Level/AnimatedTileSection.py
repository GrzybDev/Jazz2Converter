from dataclasses import dataclass


@dataclass
class AnimatedTileSection:
    Delay = 0
    DelayJitter = 0
    ReverseDelay = 0

    IsReverse = False

    Speed = 0
    FrameCount = 0

    Frames = []
