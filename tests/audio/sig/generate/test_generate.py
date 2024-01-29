import pytest
from open_jam.audio.sig.generate import normalize
import math
import numpy as np

test_normalize_params = [
    (2.3, np.array(1, 2, 3), np.array(2.3/3, 4.6/3, 2.3)),
    (1, np.array(0, 0.2, 0.1), np.array(0, 1, .5))
]

@pytest.mark.parameterize("peak, signal, expected", test_normalize_params)
def test_normalize(peak, signal, expected):
    # invoke
    actual = normalize(peak, signal)

    # assert
    for i in range(len(expected)):
        if not math.isclose(expected[i], actual[i]):
            assert(False)
    assert(True)


    