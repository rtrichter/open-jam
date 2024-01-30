import pytest
from open_jam.audio.sig.generate import get_time_vector
import math
import numpy as np
import open_jam.conversions as conv
from open_jam.config import *

test_get_time_vector_params = [
    (10/RATE, [i/RATE for i in range(10+1)]),
    (10, np.arange(0, 10*RATE+1)/RATE)
]

@pytest.mark.parametrize(
    "duration_s, expected", test_get_time_vector_params)
def test_get_time_vector(duration_s, expected):
    # invoke
    actual = get_time_vector(duration_s)
    
    # assert
    print(actual, "\n", expected)
    assert all([math.isclose(actual[i], expected[i]) for i in range(actual.size)])