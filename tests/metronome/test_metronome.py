import pytest
from open_jam.metronome.metronome import *

test_tempo_inc_tempo_params = [
    [Tempo((3, 8), 90), 10, 100],
    [Tempo((3, 8), 90), -68, 22],
    [Tempo((4, 4), 200), 20, 220]
]

@pytest.mark.parametrize("tempo, increment, expected", test_tempo_inc_tempo_params)
def test_tempo_inc_tempo(tempo, increment, expected):
    tempo.inc_bpm(increment)
    actual = tempo.bpm
    assert(expected == actual)

test_tempo_str_params = [
    [Tempo((3, 8), 90), "3/8=90"],
    [Tempo((12, 8), 70), "12/8=70"],
    [Tempo((2, 2), 150), "2/2=150"],
    [Tempo((4, 4), 184), "4/4=184"],
    [Tempo((6, 8), 71), "6/8=71"],
    [Tempo((9, 17), 948), "9/17=948"],
]

@pytest.mark.parametrize("tempo, expected", test_tempo_str_params)
def test_tempo_str(tempo, expected):
    actual = str(tempo)
    assert(expected == actual)


test_time_sig_str_params = [
    [TimeSig(4, 4), "4/4"],
    [TimeSig(3, 4), "3/4"],
    [TimeSig(2, 4), "2/4"],
    [TimeSig(6, 8), "6/8"],
    [TimeSig(12, 8), "12/8"],
    [TimeSig(2, 2), "2/2"],
]
@pytest.mark.parametrize("time_sig, expected", test_time_sig_str_params)
def test_time_sig_str(time_sig, expected):
    actual = str(time_sig)
    assert(expected == actual)

def metronome_standard(args, expected):
    m: Metronome = Metronome(*args)
    assert all([m.tempo == expected[0],
                m.time_sig == expected[1],
                m.emphasis == expected[2] ])

def metronome_raises_error(args, expected):
    with pytest.raises(ValueError) as excinfo:
        m = Metronome(*args)
    assert str(excinfo.value) == expected
        

test_metronome_init_params = [
    [[Tempo(3, 8), TimeSig(6, 8), [1, 2, 3, 4, 5, 6]], 
     [Tempo(3, 8), TimeSig(6, 8), [1, 2, 3, 4, 5, 6]],
     metronome_standard],
    [[Tempo(1,4), TimeSig(4,4), [1, 2, 3, 4, 5, 6]], 
     "pattern of length 6 does not match time signature 4/4",
     metronome_raises_error],
    [[Tempo(1,4), None, [1, 2, 3, 4, 5, 6]], 
     "pattern of length 6 does not match time signature 4/4",
     metronome_raises_error],
    [[Tempo(1,4), None, [1, 2, 3, 4]], 
     [Tempo(1, 4), TimeSig(4, 4), [1, 2, 3, 4]],
     metronome_standard],
    [[Tempo(1,4), None, None], 
     [Tempo(1, 4), TimeSig(4, 4), [5, 5, 5, 5]],
     metronome_standard],
    [[Tempo(1,4), TimeSig(3, 9), None], 
     [Tempo(1, 4), TimeSig(4, 4), [5, 5, 5]],
     metronome_standard],
]
@pytest.mark.parametrize("args, expected, func", test_metronome_init_params)
def test_metronome_init(args, expected, func):
    func(args, expected)