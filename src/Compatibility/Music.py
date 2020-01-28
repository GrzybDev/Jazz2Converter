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

    def _FileConverter__save(self, outputPath):
        super().save(outputPath)

        info("Now optimizing music file using FFMpeg...")
        subprocess.call(
            [
                "ffmpeg",
                "-i",
                self.path + ".wav",
                outputPath
                + os.path.splitext(os.path.basename(self.path))[0]
                + ".ogg",
            ]
        )
        os.remove(self.path + ".wav")
