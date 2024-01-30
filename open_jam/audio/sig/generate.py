import numpy as np
from scipy import signal
import open_jam.conversions.units as units
from numpy.typing import ArrayLike
from open_jam.config import *

# generator functions
DEFAULT_SIGNAL_FUNC = np.sin

# aliases and definitions for wave functions
sin = np.sin
cos = np.cos
square = np.square
sawtooth = signal.sawtooth

def triangle(x: float) -> np.array:
    return np.abs(signal.sawtooth(x))

# time vector things
def get_time_vector(duration_s) -> np.array:
    return np.linspace(0, duration_s, num=1+units.sec2sample(duration_s))
