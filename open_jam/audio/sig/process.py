import numpy as np
from numpy.typing import ArrayLike
import open_jam.conversions.units as units
from typing import Callable

def apply_volume_profile(profile: Callable, 
                         signal: ArrayLike, 
                         start_s: int = 0, 
                         stop_s: int = None):
    """DESTRUCTIVE
    applies a volume function to a signal between the start and stop indices

    Args:
        profile (function): function in terms of time with range = [0, 1]
        signal (ArrayLike): array to be modified by the profile
        start_s (int, optional): first time value to be modified. Defaults to 0
        stop_s (int, optional): last time value to be modified. Defaults to None
    """
    start_smp = units.sec2sample(start_s)
    stop_smp = units.sec2sample(stop_s) if not stop_s is None else len(signal)
    for i in range(start_smp, stop_smp):
        signal[i] *= profile(units.sample2sec(i))
    return signal
        
def get_normalized(peak: float, signal: np.ndarray):
    signal = signal.astype('float64')
    signal *= peak / float(np.max(np.abs(signal)))
    return signal