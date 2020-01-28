import logging

from colorama import Fore


def verbose(message):
    return logging.debug(Fore.WHITE + message + Fore.RESET)


def info(message):
    return logging.info(Fore.CYAN + message + Fore.RESET)


def warning(message):
    return logging.warning(Fore.YELLOW + message + Fore.RESET)


def error(message):
    return logging.critical(Fore.RED + message + Fore.RESET)
