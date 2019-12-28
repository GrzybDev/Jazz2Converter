import logging
from abc import ABC, abstractmethod

from src.Helpers.logger import info
from src.Utilities import File


class FileConverter(ABC):

    def __init__(self, path):
        self.file = File(open(path, "rb"))
        self.path = path

        super().__init__()

    @abstractmethod
    def convert(self):
        logging.info(info("Now converting " + self.path + "..."))

    def finish(self):
        self.file.context.close()

    @abstractmethod
    def save(self, outputPath):
        logging.info(info("Finished conversion. Now saving to " + outputPath + "..."))
