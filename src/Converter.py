import glob
import os
import sys
from multiprocessing import Process

from src.Compatibility.Anims import AnimsConverter
from src.Compatibility.Data import DataConverter
from src.Compatibility.Episode import EpisodeConverter
from src.Compatibility.Language import LanguageConverter
from src.Compatibility.Level import LevelConverter
from src.Compatibility.Music import MusicConverter
from src.Compatibility.Tileset import TilesetConverter
from src.Compatibility.Video import VideoConverter
from src.Patches.TexturePalette import TexturePalettePatcher
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

    def convert(self, option, Type, extensions):
        threads = []

        if option in self.config and self.config[option]:
            warning("Skipping " + Type + " files...")
        else:
            info("Now converting " + Type + " files...")

            outputPath = self.outputPath + "/" + Type + "/"
            os.mkdir(outputPath)

            for extension in extensions:
                for File in glob.glob(self.gamePath + "/*." + extension):
                    converter = self.converters.get(extension, None)

                    if converter is not None:
                        threads.append(Process(target=self.converter_thread, args=(converter, File, outputPath),
                                               name=Type + "Converter (" + str(os.path.basename(File)) + ")"))
                        threads[-1].start()
                    else:
                        warning("No valid converter for " + Type + " (" + extension + ") is defined!")
                        break

        for thread in threads:
            thread.join()

    @staticmethod
    def converter_thread(context, File, outputPath):
        context = context(File)
        context.convert()
        context.save(outputPath)
    
    def patch(self, file, Type):
        if Type == "Texture":
            patcher = TexturePalettePatcher(file)
            patcher.convert()
            patcher.save(file)

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
        
        self.patch(self.outputPath + "/Data/Menu.Texture.16x16.png", "Texture")
        self.patch(self.outputPath + "/Data/Menu.Texture.32x32.png", "Texture")
        self.patch(self.outputPath + "/Data/Menu.Texture.128x128.png", "Texture")
        
        info("Finished conversions!")
