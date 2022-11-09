# Balding Functions.py
# Helper functions for the bot

# Libraries
import random


# Functions
def random_color() -> hex:
    def r(): return random.randint(0, 255)
    return int('0x%02X%02X%02X' % (r(), r(), r()), 16)
