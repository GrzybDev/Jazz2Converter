import getopt
import logging
import os.path
import shutil

from colorama import init

from src.Converter import Converter
from src.ErrorCodes import SUCCESS_OK, ERROR_INVALID_ARGUMENTS, ERROR_UNKNOWN_ARGUMENT, ERROR_NOT_VALID_GAME_FOLDER, \
    ERROR_NO_GAME_FOLDER_SPECIFIED, ERROR_LAUNCHED_INCORRECTLY
from src.Logger import info, warning, verbose, error


def showHelp():
    info('Usage: run.py [-h|--help] -i|--input "GAME FOLDER" (arguments)')
    info("\n")
    info("-h | --help\t|| Shows this message")
    info("-v | --verbose\t|| Shows additional debug information")
    info("-i | --input\t|| Sets Jazz Jackrabbit 2 game folder")
    info("-o | --output\t|| Sets converted file path (Converter output folder)")
    info("-c | --clear\t|| Clears output folder before conversion (to prevent \"folder is not empty\" errors)")
    info("\n")
    info("Converter options:")
    info("--skip-languages\t|| Skips language files (*.j2s)")
    info("--skip-data\t\t|| Skip data files (*.j2d)")
    info("--skip-animations\t|| Skip animation files (*.j2a)")
    info("--skip-episodes\t|| Skip episode files (*.j2e)")
    info("--skip-music\t|| Skip music files (*.j2b, *.mod, *.it, *.s3m)")
    info("--skip-videos\t|| Skip video files (*.j2v)")
    info("--skip-tilesets\t|| Skip tileset files (*.j2t)")
    info("--skip-levels\t|| Skip level files (*.j2l)")

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
            warning("Invalid reply!")


def clearFolder(output):
    info("Clearing output folder...")

    try:
        shutil.rmtree(output)
        verbose("Folder cleared successfully!")
    except Exception as e:
        verbose("There was an error during clearing folder! (" + str(e) + ")")


def run(arguments):
    init()
    logging.getLogger().setLevel(logging.INFO)

    info("Jazz Jackrabbit 2 Converter v1.0")
    info("By Marek Grzyb (@GrzybDev) (https://github.com/GrzybDev)")
    info("Designed for Jazz Jackrabbit 2 v1.24")
    info("--------------------------------------------------------")

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
            "--skip-music": lambda: converterArgs.update(skipMusic=True),
            "--skip-videos": lambda: converterArgs.update(skipVideos=True),
            "--skip-tilesets": lambda: converterArgs.update(skipTilesets=True),
            "--skip-levels": lambda: converterArgs.update(skipLevels=True),
        }

        try:
            opts, args = getopt.getopt(
                arguments[1:],
                "hvi:o:c",
                [
                    "help",
                    "verbose",
                    "input=",
                    "output=",
                    "clear",
                    "skip-languages",
                    "skip-data",
                    "skip-animations",
                    "skip-episodes",
                    "skip-music",
                    "skip-videos",
                    "skip-tilesets",
                    "skip-levels",
                ],
            )
        except getopt.GetoptError:
            error("Invalid arguments provided!\n"
                  "Run program without parameters to enter interactive mode or check --help for usage")
            return ERROR_INVALID_ARGUMENTS

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                return showHelp()
            elif opt in ("-v", "--verbose"):
                logging.getLogger().setLevel(logging.DEBUG)
            elif opt in ("-i", "--input"):
                gameFolder = arg
            elif opt in ("-o", "--output"):
                outputFolder = arg
            elif opt in ("-c", "--clear"):
                clearOutputFolder = True
            elif opt in (
                    "--skip-languages",
                    "--skip-data",
                    "--skip-animations",
                    "--skip-episodes",
                    "--skip-music",
                    "--skip-videos",
                    "--skip-tilesets",
                    "--skip-levels",
            ):
                knownArgs.get(opt)()
            else:
                error("Got unknown argument: " + opt +
                      "\nRun program without parameters to enter interactive mode or check --help for usage")
                return ERROR_UNKNOWN_ARGUMENT

        if gameFolder is not None or outputFolder is not None:
            if os.path.exists(gameFolder) and (
                    os.path.exists(gameFolder + "/Jazz2.exe")
                    and os.path.isfile(gameFolder + "/Jazz2.exe")
            ):
                pass
            else:
                error("Folder you specified: " + gameFolder +
                      " is not valid Jazz Jackrabbit 2 Game Folder!")
                return ERROR_NOT_VALID_GAME_FOLDER
        else:
            error("You didn't specified game or output folder!")
            return ERROR_NO_GAME_FOLDER_SPECIFIED
    else:
        validGameFolder = False

        while not validGameFolder:
            gameFolder = input("Please enter Jazz Jackrabbit 2 game directory: ")

            if os.path.exists(gameFolder) and (
                    os.path.exists(gameFolder + "/Jazz2.exe")
                    and os.path.isfile(gameFolder + "/Jazz2.exe")
            ):
                validGameFolder = True
            else:
                warning("Folder you specified: " + gameFolder +
                        " is not valid Jazz Jackrabbit 2 Game Folder!")

        while outputFolder is None:
            outputFolder = input("Please enter path where to put converted files: ")

        clearOutputFolder = getBooleanFromUser("Clear output folder?")

        converterArgs.update(skipLangs=not getBooleanFromUser("Convert language files (*.j2s)?"))
        converterArgs.update(skipData=not getBooleanFromUser("Convert data files (*.j2d)?"))
        converterArgs.update(skipAnims=not getBooleanFromUser("Convert animation files (*.j2a)?"))
        converterArgs.update(skipEpisodes=not getBooleanFromUser("Convert episode files (*.j2e)?"))
        converterArgs.update(skipMusic=not getBooleanFromUser("Convert music files (*.j2b, *.mod, *.it, *.s3m)?"))
        converterArgs.update(skipVideos=not getBooleanFromUser("Convert video files (*.j2v)?"))
        converterArgs.update(skipTilesets=not getBooleanFromUser("Convert tileset files (*.j2t)?"))
        converterArgs.update(skipLevels=not getBooleanFromUser("Convert levels files (*.j2l)?"))

    if clearOutputFolder:
        clearFolder(outputFolder)

    Converter(converterArgs, gameFolder, outputFolder).run()
    return SUCCESS_OK


if __name__ == "__main__":
    error("You have to run Jazz2Converter using run.py located in root directory!")
    exit(ERROR_LAUNCHED_INCORRECTLY)
