from fractions import Fraction
from os import path
METRO_PATH = path.split(__file__)[0]

# Defaults
DEFAULT_SOUND = path.join(METRO_PATH, "sounds/default.wav")
# DEFAULT_EMPHASIS_SOUND = path.join(METRO_PATH, "sounds/1b_click.mp3")
DEFAULT_SIGNATURE = (4, 4)
DEFAULT_TEMPO = (Fraction(1, 4), 60)