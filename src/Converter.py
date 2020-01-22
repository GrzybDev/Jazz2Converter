import glob
import logging
import os
import sys

from pathlib import Path

from src.Helpers.logger import *
from src.Helpers.errors import ERROR_OUTPUT_IS_NOT_DIRECTORY, ERROR_OUTPUT_IS_NOT_EMPTY
from src.Formats import *


class Converter(object):

    converters = {
        "j2s": LanguageConverter,
        "j2d": DataConverter,
        "j2a": AnimsConverter,
        "j2e": EpisodeConverter,
        "j2b": MusicConverter,
        "mod": MusicConverter,
        "it": MusicConverter,
        "s3m": MusicConverter,
        "j2v": VideoConverter,
        "j2t": TilesetConverter,
        "j2l": LevelConverter
    }

    def __init__(self, config, gamePath, outputPath):
        self.config = config
        self.gamePath = gamePath
        self.outputPath = outputPath

    def __prepare(self):
        logging.debug(verbose("Preparing output folder..."))

        if not os.path.exists(self.outputPath):
            logging.warning(warning("Selected output folder doesn't exist! Creating it..."))
            os.makedirs(self.outputPath)
        else:
            if len(os.listdir(self.outputPath)) != 0:
                logging.critical(error("Output folder is not empty!"))
                sys.exit(ERROR_OUTPUT_IS_NOT_EMPTY)
            else:
                if not os.path.isdir(self.outputPath):
                    logging.critical(error("Output path is not directory!"))
                    sys.exit(ERROR_OUTPUT_IS_NOT_DIRECTORY)

    def convert(self, option, type, extensions):
        if option in self.config and self.config[option]:
            logging.warning(warning("Skipping " + type + " files..."))
        else:
            logging.info(info("Now converting " + type + " files..."))

            outputPath = self.outputPath + "/" + type + "/"
            os.mkdir(outputPath)

            for extension in extensions:
                for file in glob.glob(self.gamePath + "/*." + extension):
                    converter = self.converters.get(extension, None)

                    if converter is not None:
                        converter = converter(file)
                        converter.convert()
                        converter.save(outputPath)
                    else:
                        logging.warning(warning("No valid converter for " + type + " "
                                                "(" + extension + ") is defined!"))
                        break

    def run(self):
        self.__prepare()

        self.convert("skipLangs", "Language", ["j2s"])
        self.convert("skipData", "Data", ["j2d"])
        self.convert("skipAnims", "Anims", ["j2a"])
        self.convert("skipEpisodes", "Episodes", ["j2e"])
        self.convert("skipMusic", "Music", ["j2b", "mod", "it", "s3m"])
        self.convert("skipVideos", "Videos", ["j2v"])
        self.convert("skipTilesets", "Tilesets", ["j2t"])
        self.convert("skipLevels", "Levels", ["j2l"])

        logging.info(info("Finished conversions!"))
