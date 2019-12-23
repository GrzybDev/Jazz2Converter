import logging

from src.errors import SUCCESS_OK, ERROR_INVALID_ARGUMENTS, ERROR_UNKNOWN_ARGUMENT
from src.logger import error, info

logging.basicConfig(format="[%(module)s] %(message)s")


def showHelp():
    logging.info(info("Usage: run.py [-h|--help] -i|--input \"GAME FOLDER\" (arguments)"))
    logging.info("\n")
    logging.info(info("-h | --help || Shows this message"))
    logging.info(info("-v | --verbose || Shows additional debug information"))
    logging.info(info("-i | --input || Sets Jazz Jackrabbit 2 game folder"))
    logging.info("\n")
    logging.info(info("Converter options:"))
    logging.info(info("--skip-languages || Skips language files (*.j2s)"))
    return SUCCESS_OK


if __name__ == "__main__":
    logging.critical(error("You have to run Jazz2Converter using run.py located in root directory!"))
