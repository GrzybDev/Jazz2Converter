import logging
import getopt
import shutil
import os.path

from src.Helpers.errors import *
from src.Helpers.logger import *
from src.Converter import Converter

logging.basicConfig(format="[%(module)s] %(message)s")


def showHelp():
    print(info("Usage: run.py [-h|--help] -i|--input \"GAME FOLDER\" (arguments)"))
    print("\n")
    print(info("-h | --help\t|| Shows this message"))
    print(info("-v | --verbose\t|| Shows additional debug information"))
    print(info("-i | --input\t|| Sets Jazz Jackrabbit 2 game folder"))
    print(info("-o | --output\t|| Sets converted file path (Converter output folder)"))
    print("\n")
    print(info("Converter options:"))
    print(info("--skip-languages\t|| Skips language files (*.j2s)"))
    print(info("--skip-data\t\t|| Skip data files (*.j2d)"))
    print(info("--skip-animations\t|| Skip animation files (*.j2a)"))
    print(info("--skip-episodes\t|| Skip episode files (*.j2e)"))
    print(info("--skip-music\t|| Skip music files (*.j2b, *.mod, *.it, *.s3m)"))

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

def clearFolder(output):
    logging.info(info("Clearing output folder..."))

    try:
        shutil.rmtree(output)
        logging.debug(verbose("Folder cleared successfully!"))
    except Exception as e:
        logging.debug(verbose("There was an error during clearing folder! (" + str(e) + ")"))


def run(arguments):
    logging.getLogger().setLevel(logging.INFO)
    print(info("Jazz Jackrabbit 2 Converter v1.0"))
    print(info("By Marek Grzyb (@GrzybDev) (https://github.com/GrzybDev)"))
    print(info("Designed for Jazz Jackrabbit 2 v1.24"))
    print(info("--------------------------------------------------------"))

    converterArgs = {}
    gameFolder = None
    outputFolder = None
    clearOutputFolder = False

    if len(arguments) > 1:
        knownArgs = {
            "--skip-languages": lambda: converterArgs.update(skipLangs=True),
            "--skip-data": lambda: converterArgs.update(skipData=True),
            "--skip-animations": lambda: converterArgs.update(skipAnims=True),
            "--skip-episodes": lambda: converterArgs.update(skipEpisodes=True),
            "--skip-music": lambda: converterArgs.update(skipMusic=True)
        }

        try:
            opts, args = getopt.getopt(arguments[1:], "hvi:o:c", ["help", "verbose", "input=", "output=", "clear",
                                                                 "skip-languages", "skip-data", "skip-animations",
                                                                 "skip-episodes", "skip-music"])
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
            elif opt in ('-o', "--output"):
                outputFolder = arg
            elif opt in ('-c', "--clear"):
                clearOutputFolder = True
            elif opt in ("--skip-languages",
                         "--skip-data",
                         "--skip-animations",
                         "--skip-episodes",
                         "--skip-music"):
                knownArgs.get(opt)()
            else:
                print(error("Got unknown argument: " + opt + "\n"
                            "Run program without parameters to enter interactive mode or check --help for usage"))
                return ERROR_UNKNOWN_ARGUMENT

        if gameFolder is not None or outputFolder is not None:
            if os.path.exists(gameFolder) and (os.path.exists(gameFolder + "/Jazz2.exe")
                                               and os.path.isfile(gameFolder + "/Jazz2.exe")):
                pass
            else:
                print(error("Folder you specified: " + gameFolder + " is not valid Jazz Jackrabbit 2 Game Folder!"))
                return ERROR_NOT_VALID_GAME_FOLDER
        else:
            print(error("You didn't specified game or output folder!"))
            return ERROR_NO_GAME_FOLDER_SPECIFIED
    else:
        validGameFolder = False

        while not validGameFolder:
            gameFolder = input("Please enter Jazz Jackrabbit 2 game directory: ")

            if os.path.exists(gameFolder) and (os.path.exists(gameFolder + "/Jazz2.exe")
                                               and os.path.isfile(gameFolder + "/Jazz2.exe")):
                validGameFolder = True
            else:
                print(warning("Folder you specified: " + gameFolder + " is not valid Jazz Jackrabbit 2 Game Folder!"))

        while outputFolder is None:
            outputFolder = input("Please enter path where to put converted files: ")

        clearOutputFolder = getBooleanFromUser("Clear output folder?")
        converterArgs.update(skipLangs=not getBooleanFromUser("Convert language files (*.j2s)?"))
        converterArgs.update(skipData=not getBooleanFromUser("Convert data files (*.j2d)?"))
        converterArgs.update(skipAnims=not getBooleanFromUser("Convert animation files (*.j2a)?"))
        converterArgs.update(skipEpisodes=not getBooleanFromUser("Convert episode files (*.j2e)?"))
        converterArgs.update(skipMusic=not getBooleanFromUser("Convert music files (*.j2b, *.mod, *.it, *.s3m)?"))

    if clearOutputFolder:
        clearFolder(outputFolder)

    Converter(converterArgs, gameFolder, outputFolder).run()
    return SUCCESS_OK


if __name__ == "__main__":
    print(error("You have to run Jazz2Converter using run.py located in root directory!"))
