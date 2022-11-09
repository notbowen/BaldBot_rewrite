# Logging.py
# In charge of sending log messages

import termcolor
import os

if os.name == "nt":
    # If windows
    import colorama
    colorama.init()  # Enable colours to be printed to screen

def plus(msg: str) -> None:
    """ Used for INFO, LOGGING """
    print("[" + termcolor.colored("+", "green") + "] " + msg)

def minus(msg: str) -> None:
    """ Used for ERROR, FATAL """
    print("[" + termcolor.colored("-", "red") + "] " + msg)

def star(msg: str) -> None:
    """ Used for WARN """
    print("[" + termcolor.colored("*", "yellow") + "] " + msg)