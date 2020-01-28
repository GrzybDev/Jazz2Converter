from abc import ABC, abstractmethod

from src.Logger import info, error
from src.Utilities.File import File


class FileConverter(ABC):
    def __init__(self, path):
        self.file = File(open(path, "rb"))
        self.path = path

        super().__init__()

    def convert(self):
        try:
            info("Now converting " + self.path + "...")
            self.__convert()
        except Exception as e:
            error("Unexpected error happened while converting file: " + self.path + "! " +
                  "(" + str(e) + ")")
            self.finish()

    @abstractmethod
    def __convert(self):
        pass

    def finish(self):
        self.file.context.close()

    def save(self, outputPath):
        try:
            info("Finished conversion. Now saving to " + outputPath + "...")
            self.__save(outputPath)
        except Exception as e:
            error("Unexpected error happened during extraction process of file: " + self.path + "!" +
                  "(" + str(e) + ")")
            self.finish()

    @abstractmethod
    def __save(self, outputPath):
        pass
