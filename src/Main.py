import logging

logging.basicConfig(format="[%(module)s] %(message)s")


def run():
    logging.info()
    return 0


if __name__ == "__main__":
    logging.critical("You have to run Jazz2Converter using run.py located in root directory!")
    raise RuntimeError("Launched app without run.py")
