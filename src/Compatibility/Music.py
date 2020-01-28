import logging
import os
import subprocess

from src.Helpers.logger import *
from src.Utilities import FileConverter

class MusicConverter(FileConverter):

    def __init__(self, path):
        super().__init__(path)
        self.finish()  # File access is not required in this converter (External in use)

    def convert(self):
        super().convert()

        try:
            logging.info("Converting music file using openmpt123...")
            subprocess.call(["openmpt123", self.path, "--render"])
        except FileNotFoundError:
            logging.error(error("openmpt123 is not accessible, please install it system-wise or place it in current folder!"))
        except Exception as e:
            logging.error(error("Unexpected error happened during conversion! (" + str(e) + ")")) 
    
    def save(self, outputPath):
        super().save(outputPath)

        try:
            logging.info("Now optimizing music file using FFMpeg...")
            subprocess.call(["ffmpeg", "-i", self.path + ".wav", outputPath + os.path.splitext(os.path.basename(self.path))[0] + ".ogg"])
            os.remove(self.path + ".wav")
        except FileNotFoundError:
            logging.error(error("FFMpeg is not accessible, please install it system-wise or place it in current folder!"))
        except Exception as e:
            logging.error(error("Unexpected error happened during optimization! (" + str(e) + ")"))