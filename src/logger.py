from colorama import init, Fore

init()


def verbose(message):
    return Fore.WHITE + message + Fore.RESET


def info(message):
    return Fore.CYAN + message + Fore.RESET


def warning(message):
    return Fore.YELLOW + message + Fore.RESET


def error(message):
    return Fore.RED + message + Fore.RESET
