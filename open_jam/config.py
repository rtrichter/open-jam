import pyaudio
import time
from os import path

# UPPER_CASE are constants. snake_case can change at runtime

# audio_io
RATE = 44100
CHANNELS = 1
CHUNK = 1024
FORMAT = pyaudio.paFloat32

volume = 0.5

# system
START_TIME = time.time()

# CLASS FOR NAMESPACE ONLY
class PATHS:
    ASSETS = "assets"
    SOUNDS = path.join(ASSETS, "sounds")
    METRONOME = path.join(SOUNDS, "metronome")
