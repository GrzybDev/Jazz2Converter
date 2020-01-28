from dataclasses import dataclass


@dataclass
class LevelEntry:
    LevelName = ""
    MinTextID, MaxTextID = (0, 0)
    LevelOffset = 0

    HelpStrings = []
