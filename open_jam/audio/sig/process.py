import numpy as np
from numpy.typing import ArrayLike
import conversions as conv

def apply_volume_profile(profile: function, 
                         signal: ArrayLike, 
                         start_s: int = 0, 
                         stop_s: int = None):
    """DESTRUCTIVE
    applies a volume function to a signal between the start and stop indices

    Args:
        profile (function): function in terms of time and range = [0, 1]
        signal (ArrayLike): array to be modified by the profile
        start_s (int, optional): first time value to be modified. Defaults to 0
        stop_s (int, optional): last time value to be modified. Defaults to None
    """
    start_smp = conv.sec2samples(start_s)
    stop_smp = conv.sec2samples(stop_s) if not stop_s is None else len(signal)
    for i in range(start_smp, stop_smp):
        signal[i] *= profile(i)
        