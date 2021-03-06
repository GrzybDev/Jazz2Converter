import os
import subprocess

from src.Logger import info
from src.Utilities.FileConverter import FileConverter


class MusicConverter(FileConverter):
    def __init__(self, path):
        super().__init__(path)
        self.finish()  # File access is not required in this converter (External in use)

    def _FileConverter__convert(self):
        info("Converting music file using openmpt123...")
        subprocess.call(["openmpt123", self.path, "--render"])
        subprocess.call(["sync"])  # Warning: It might temporarily slow down computer
        # I'm using forcing disk sync because FFMpeg can start reading files BEFORE it's being fully saved on disk.
        # ...And that causes audio cut after some time

        # On windows sync program are available here: https://docs.microsoft.com/sysinternals/downloads/sync

    def _FileConverter__save(self, outputPath):
        info("Now optimizing music file using FFMpeg...")
        subprocess.call(
            [
                "ffmpeg",
                "-i",
                self.path + ".wav",
                outputPath
                + os.path.splitext(os.path.basename(self.path))[0]
                + ".wav",
            ]
        )
        os.remove(self.path + ".wav")
