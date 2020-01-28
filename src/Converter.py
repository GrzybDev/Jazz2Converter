import glob
import os
import sys
import threading

from src.Compatibility.Anims import AnimsConverter
from src.Compatibility.Data import DataConverter
from src.Compatibility.Episode import EpisodeConverter
from src.Compatibility.Language import LanguageConverter
from src.Compatibility.Level import LevelConverter
from src.Compatibility.Music import MusicConverter
from src.Compatibility.Tileset import TilesetConverter
from src.Compatibility.Video import VideoConverter
from src.ErrorCodes import ERROR_OUTPUT_IS_NOT_DIRECTORY, ERROR_OUTPUT_IS_NOT_EMPTY
from src.Logger import info, verbose, warning, error


class Converter(object):
    converters = {
        "j2a": AnimsConverter,
        "j2d": DataConverter,
        "j2e": EpisodeConverter,
        "j2s": LanguageConverter,
        "j2l": LevelConverter,
        "j2b": MusicConverter,
        "mod": MusicConverter,
        "it": MusicConverter,
        "s3m": MusicConverter,
        "j2v": VideoConverter,
        "j2t": TilesetConverter,
    }

    def __init__(self, config, gamePath, outputPath):
        self.config = config
        self.gamePath = gamePath
        self.outputPath = outputPath

        self.__prepare()

    def __prepare(self):
        verbose("Preparing output folder...")

        if not os.path.exists(self.outputPath):
            warning("Selected output folder doesn't exist! Creating it...")
            os.makedirs(self.outputPath)
        else:
            if len(os.listdir(self.outputPath)) != 0:
                error("Output folder is not empty!")
                sys.exit(ERROR_OUTPUT_IS_NOT_EMPTY)
            else:
                if not os.path.isdir(self.outputPath):
                    error("Output path is not directory!")
                    sys.exit(ERROR_OUTPUT_IS_NOT_DIRECTORY)

    def convert(self, option, type, extensions):
        threads = []

        if option in self.config and self.config[option]:
            warning("Skipping " + type + " files...")
        else:
            info("Now converting " + type + " files...")

            outputPath = self.outputPath + "/" + type + "/"
            os.mkdir(outputPath)

            for extension in extensions:
                for file in glob.glob(self.gamePath + "/*." + extension):
                    converter = self.converters.get(extension, None)

                    if converter is not None:
                        converter = converter(file)
                        threads.append(threading.Thread(target=self.converter_thread, args=(converter, outputPath)))
                        threads[-1].start()
                    else:
                        warning("No valid converter for " + type + " (" + extension + ") is defined!")
                        break

        for thread in threads:
            thread.join()

    @staticmethod
    def converter_thread(context, outputPath):
        context.convert()
        context.save(outputPath)

    def run(self):
        info("Starting conversions...")

        self.convert("skipData", "Data", ["j2d"])
        self.convert("skipAnims", "Anims", ["j2a"])
        self.convert("skipEpisodes", "Episodes", ["j2e"])
        self.convert("skipLangs", "Language", ["j2s"])
        self.convert("skipLevels", "Levels", ["j2l"])
        self.convert("skipMusic", "Music", ["j2b", "mod", "it", "s3m"])
        self.convert("skipTilesets", "Tilesets", ["j2t"])
        self.convert("skipVideos", "Videos", ["j2v"])

        info("Finished conversions!")
