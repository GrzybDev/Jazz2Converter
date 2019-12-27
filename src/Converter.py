import glob
import logging
import os
import sys

from pathlib import Path

from src.Helpers.logger import *
from src.Helpers.errors import ERROR_OUTPUT_IS_NOT_DIRECTORY, ERROR_OUTPUT_IS_NOT_EMPTY
from src.Formats.Language import LanguageConverter


class Converter(object):

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

    def run(self):
        self.__prepare()

        if "skipLangs" in self.config and self.config["skipLangs"]:
            logging.debug(verbose("Skipping language files..."))
        else:
            logging.info(info("Now converting language files..."))

            os.mkdir(self.outputPath + "/Languages")

            for file in glob.glob(self.gamePath + "/*.j2s"):
                converter = LanguageConverter(file)
                converter.convert()
                converter.save(self.outputPath + "/Languages/" + Path(file).name.split(".j2s")[0] + ".json")
