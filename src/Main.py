import logging
import getopt

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


def run(arguments):
    logging.getLogger().setLevel(logging.INFO)
    logging.info(info("Jazz Jackrabbit 2 Converter v1.0"))
    logging.info(info("By Marek Grzyb (@GrzybDev) (https://github.com/GrzybDev)"))
    logging.info(info("Designed for Jazz Jackrabbit 2 v1.24"))
    logging.info(info("--------------------------------------------------------"))

    converterArgs = {}
    gameFolder = None

    if len(arguments) > 1:
        knownArgs = {
            "--skip-languages": lambda: converterArgs.update(skipLangs=True)
        }

        try:
            opts, args = getopt.getopt(arguments[1:], "hvi:", ["help", "verbose", "input=",
                                                               "skip-languages"])
        except getopt.GetoptError:
            logging.critical(error("Invalid arguments provided!\n"
                                   "Run program without parameters to enter interactive mode or check --help for usage"))
            return ERROR_INVALID_ARGUMENTS

        for opt, arg in opts:
            if opt in ('-h', "--help"):
                return showHelp()
            elif opt in ('-v', "--verbose"):
                logging.getLogger().setLevel(logging.DEBUG)
            elif opt in ('-i', "--input"):
                gameFolder = arg
            elif opt in ("--skip-languages"):
                knownArgs.get(opt)()
            else:
                logging.critical(error("Got unknown argument: " + opt + "\n"
                                       "Run program without parameters to enter interactive mode or check --help for usage"))
                return ERROR_UNKNOWN_ARGUMENT
    else:
        # TODO: Interactive mode
        raise NotImplementedError

    return SUCCESS_OK


if __name__ == "__main__":
    logging.critical(error("You have to run Jazz2Converter using run.py located in root directory!"))
