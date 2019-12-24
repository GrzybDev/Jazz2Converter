import logging
import getopt
import os.path

from src.errors import SUCCESS_OK, ERROR_INVALID_ARGUMENTS, ERROR_UNKNOWN_ARGUMENT
from src.logger import error, info, warning

logging.basicConfig(format="[%(module)s] %(message)s")


def showHelp():
    print(info("Usage: run.py [-h|--help] -i|--input \"GAME FOLDER\" (arguments)"))
    print("\n")
    print(info("-h | --help || Shows this message"))
    print(info("-v | --verbose || Shows additional debug information"))
    print(info("-i | --input || Sets Jazz Jackrabbit 2 game folder"))
    print("\n")
    print(info("Converter options:"))
    print(info("--skip-languages || Skips language files (*.j2s)"))
    return SUCCESS_OK


def getBooleanFromUser(question):
    while True:
        reply = input(question + " ").lower().strip()

        if reply == "y" or reply == "yes" or reply == "n" or reply == "no":
            if reply[0] == "y":
                return True
            else:
                return False
        else:
            print(warning("Invalid reply!"))


def run(arguments):
    logging.getLogger().setLevel(logging.INFO)
    print(info("Jazz Jackrabbit 2 Converter v1.0"))
    print(info("By Marek Grzyb (@GrzybDev) (https://github.com/GrzybDev)"))
    print(info("Designed for Jazz Jackrabbit 2 v1.24"))
    print(info("--------------------------------------------------------"))

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
            print(error("Invalid arguments provided!\n"
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
                print(error("Got unknown argument: " + opt + "\n"
                            "Run program without parameters to enter interactive mode or check --help for usage"))
                return ERROR_UNKNOWN_ARGUMENT
    else:
        # TODO: Interactive mode
        raise NotImplementedError

    return SUCCESS_OK


if __name__ == "__main__":
    print(error("You have to run Jazz2Converter using run.py located in root directory!"))
