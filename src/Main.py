import logging

from src.logger import error, info
logging.basicConfig(format="[%(module)s] %(message)s")


def run():
    logging.info()
    return 0


if __name__ == "__main__":
    logging.critical(error("You have to run Jazz2Converter using run.py located in root directory!"))
