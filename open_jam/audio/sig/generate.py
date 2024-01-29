import numpy as np
from scipy import signal
import conversions as conv
from numpy.typing import ArrayLike

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
def get_time_vector(duration_s, offset_rad: float = None) -> np.array:
    return np.linspace(0+offset_rad,
                       conv.sec2samples(duration_s),
                       num=1+conv.sec2samples(duration_s))

def normalize(peak: float, signal: ArrayLike):
    signal *= peak / np.max(np.abs(signal))