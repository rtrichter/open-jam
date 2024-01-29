import numpy as np
from scipy import signal

# generator functions
DEFAULT_SIGNAL_FUNC = np.sin

# aliases and definitions for wave functions
sin = np.sin
cos = np.cos
square = np.square
sawtooth = signal.sawtooth

def triangle(x):
    return np.abs(signal.sawtooth(x))

# time vector things
def get_time_vector()