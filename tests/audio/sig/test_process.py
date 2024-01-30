import pytest
from open_jam.audio.sig.process import get_normalized, apply_volume_profile
import math
import numpy as np
from open_jam.config import *

test_get_normalized_params = [
    (2.3, np.array((1, 2, 3)), np.array((2.3/3, 4.6/3, 2.3))),
    (1, np.array((0, 0.2, 0.1)), np.array((0, 1, .5)))
]

@pytest.mark.parametrize("peak, signal, expected", test_get_normalized_params)
def test_get_normalized(peak, signal, expected):
    # invoke
    actual = get_normalized(peak, signal)

    # assert
    assert all([math.isclose(expected[i], actual[i]) for i in range(len(expected))])

    
def test_apply_volume_profile():
    # setup
    profile = lambda t: t*RATE/10
    signal = np.ones(10*RATE)*10
    start = 0
    stop = None # invokes default value behavior
    expected = np.arange(0, 10*RATE)

    # invoke
    actual = apply_volume_profile(profile, signal, start, stop)

    # analyze
    print(actual[:10], "\n", expected[:10])
    assert all([math.isclose(actual[i], expected[i]) for i in range(len(expected))])
    
    
    