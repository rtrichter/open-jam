import random
import pyaudio
import numpy as np
import time

NOTES = list("ABCDEFG")
MOD = ["", "b", "#"] # could add x (double sharp) or bb later, "" = no mod
INTERVALS = ["P1", "m2", "M2", "m3", "M3", "P4", "TT",
             "P5", "m6", "M6", "m7", "M7", "P8"]
INTERVALS_N = ["0", "b2", "2", "b3", "3", "4", "b5", 
               "5", "b6", "6", "b7", "7", "8"]
VOLUME = 0.5
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100

# class Interval:

#     __slots__ = ["semitones", "mmp_name", "mmp_short", "ad_name", "ad_short",
#                  "names", "degree"]


#     def __init__(self, semitones, mmp_name, mmp_short, ad_name, ad_short, names,
#                  degree):
#         self.semitones = semitones
#         self.mmp_name = mmp_name
#         self.mmp_short = mmp_short
#         self.ad_name = ad_name
#         self.ad_short = ad_short
#         self.names = names
#         self.degree = degree


# class Intervals(Enum):
#     UNISON = Interval(0, "perfect unison", "1", ),
#     MINOR_SECOND = Interval(1),
#     MAJOR_SECOND = Interval(2),
#     MINOR_THIRD = Interval(3),
#     MAJOR_THIRD = Interval(4),
#     PERFECT_FOURTH = Interval(5),
#     TRITONE = Interval(6),
#     PERFECT_FIFTH = Interval(7),
#     MINOR_SIXTH = Interval(8),
#     MAJOR_SIXTH = Interval(9),
#     MINOR_SEVENTH = Interval(10),
#     MAJOR_SEVENTH = Interval(11),
#     PERFECT_OCTAVE = Interval(12)

def get_random_note(use_mod=True):
    return random.choice(NOTES) + random.choice(MOD)

def get_random_interval(use_name=False):
    return random.choice(INTERVALS) if use_name else random.choice(INTERVALS_N)

def get_interval_sequence(length, use_name=False):
    return [get_random_interval(use_name=use_name) for i in range(length)]

def interval_to_semitones(interval):
    for i in range(len(INTERVALS)):
        if interval == INTERVALS[i]:
            return i
    for i in range(len(INTERVALS_N)):
        if interval == INTERVALS_N[i]:
            return i
    return -1


def get_playable_note(frequency, duration):
    duration_ms = int(duration * 1000)
    time_vec = np.linspace(0, duration_ms, num=(RATE//1000)*duration_ms+1) / 1000
    sig = np.sin(frequency * 2*np.pi*time_vec)
    sig = sig.astype(np.float32)

    # START apply_volume_profile
    # clean up beginning and end
    transition = 0.05
    ends = int(RATE*transition)
    print(RATE*transition)
    for i in range(ends):
        sig[-i] *= i/ends
        sig[i] *= i/ends
    # END apply_volume_profile

        
    output_bytes = (VOLUME * sig).tobytes()
    return output_bytes

def play_intervals(intervals, start, duration, separation):
    """Requires semitone-intervals"""
    duration -= separation
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)
    for i in range(4):
        data = get_playable_note(start, 2*duration)
        stream.write(data)
        time.sleep(separation*2)
    for interval in intervals:
        data = get_playable_note(int(start * (1 + interval/12)), duration)
        stream.write(data)
        time.sleep(separation)
    
    stream.close()
    p.terminate()
        


intervals = get_interval_sequence(10, True)
print(intervals)
semi = [interval_to_semitones(interval) for interval in intervals]
print(semi)
play_intervals(semi, 440, 0.25, 0.00)

