import numpy as np
from scipy import fftpack
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import simpleaudio as sa
from dataclasses import dataclass
from random import randint
from scipy import signal
import time

SAMPLE_RATE = 44100



def get_wave(freq, amp, time_vec=None, noise_weight=0, func=np.sin, angle=0):
    if time_vec is None:
        time_vec = np.linspace(0, 10, num=SAMPLE_RATE*10)
    # amp is scaling the sine wave amplitude
    # np.sin() is generating a wave (np.array) for each point in time_vec
    # freq is scaling the frequency
    # 2*np.pi*time_vec allows us to use Hz as frequency inputs 
    # 1Hz * 2pi * 1s -> takes 1 second for 1 cycle = 1Hz wave
    return ((1+np.sin(100*2*np.pi*time_vec))*.2+.9) * amp*(func(angle + freq*2*np.pi*time_vec) + noise_weight*np.random.randn(time_vec.size))

# this is was stupid and unecessary... don't keep it later
@dataclass
class FFT_Data:
    amplitude: np.array
    power: np.array
    angle: np.array
    sample_freq: np.array
    amp_freq: np.array
    amp_position: np.array
    peak: int


def get_fft(sig, time_vec):
    # scipy magic
    sig_fft = fftpack.fft(sig)

    # amplitude of each frequency. use sample_freq (below) to lookup the frequency
    # at a given index 
    # (amplitude[i] is the amplitude at frequency sample_freq[i])
    amplitude = np.abs(sig_fft)[:time_vec.size//2]
    # power spectrum (idk what this is)
    power = amplitude**2
    # angle spectrum (also don't know what this is)
    angle = np.angle(sig_fft)[:time_vec.size//2]

    # get an array of frequencies (as mentioned above)
    sample_freq = fftpack.fftfreq(sig.size, d=time_vec[1]-time_vec[0])[:time_vec.size//2]

    # not sure what the rest of this is doing but it is to find the peak frequency
    # which is the "true pitch" of a wave
    amp_freq = np.array([amplitude, sample_freq])

    # positions of the maximum amplitudes
    amp_position = amp_freq[0,:].argmax()

    # frequency at maximum positions
    peak_frequency = amp_freq[1, amp_position] # get the primary pitch

    # return the things
    return FFT_Data(amplitude, power, angle, sample_freq, amp_freq[0], amp_position, peak_frequency)

def show_fft(sig, time_vec):
    # just simple matplot stuff
    data : FFT_Data = get_fft(sig, time_vec)
    print(data.peak)
    plt.figure()
    plt.plot(data.sample_freq, data.amp_freq)
    plt.show()
    
def get_time_vec(duration_s, random_offset=False):
    # take a space of time from 0 to duration_s
    # split it into SAMPLE_RATE*duration_s equal parts
    # this gives you evenly spaced time values to use later
    # ie np.linspace(0, 4, 9) = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
    # imagine sample rate of 2 and duration 4 (num=9)
    # this seems weird but 0 and 4 are both included in the linspace so there are 
    # 9 even elements in the 0 to 4 range
    offset = randint(0, SAMPLE_RATE) * random_offset
    return np.linspace(0+offset, duration_s+offset, num=SAMPLE_RATE*duration_s+1)

def get_processed_sig(sig):
    # use this when generating signals with numpy (get_wave(...), time_vec, etc)
    # otherwise it sounds like static
    sig *= 32767 / np.max(np.abs(sig)) # normalize to 16 bit range
    sig = sig.astype(np.int16) # convert to 16 bit data
    return sig
    

def wav_to_array(filename):
    f = read(filename)
    f = np.array(f[1], dtype=float)
    return f

def time_vec_from_sig(sig, sample_rate=SAMPLE_RATE):
    return np.linspace(0, sig.size/sample_rate, sig.size)
    
    
def show_fan_sound_fft():
    f = wav_to_array("audio/background.wav")
    time_vec = time_vec_from_sig(f)
    show_fft(f, time_vec)


def simulate_fan_sound(duration_s):
    # numbers to simulate the sound of my fan (it gets surprisingly close for only
    # a few frequencies)
    freq_1 = 225.5
    amp_1 = 2.6 * 10**8
    freq_2 = 57
    amp_2 = 1.8 * 10**8
    freq_3 = 120
    amp_3 = 1.45 * 10**8
    freq_4 = 104
    amp_4 = 6.4 * 10**7
    freq_5 = 282
    amp_5 = 7.6 * 10**7
    freq_6 = 339
    amp_6 = 5.28 * 10**7
    freq_7 = 207
    amp_7 = 5.4 * 10**7
    freq_8 = 180
    amp_8 = 3.9 * 10**8
    freq_9 = 151
    amp_9 = 6.1

    time_vec = get_time_vec(duration_s)
    sigs = []
    sigs.append(get_wave(freq_1, amp_1, get_time_vec(duration_s)))
    sigs.append(get_wave(freq_2, amp_2, get_time_vec(duration_s)))
    sigs.append(get_wave(freq_3, amp_3, get_time_vec(duration_s)))
    sigs.append(get_wave(freq_4, amp_4, get_time_vec(duration_s)))
    sigs.append(get_wave(freq_5, amp_5, get_time_vec(duration_s)))
    sigs.append(get_wave(freq_6, amp_6, get_time_vec(duration_s)))
    sigs.append(get_wave(freq_7, amp_7, get_time_vec(duration_s)))
    sigs.append(get_wave(freq_8, amp_8, get_time_vec(duration_s)))
    sigs.append(get_wave(freq_9, amp_9, get_time_vec(duration_s)))
    sig = sum(sigs)

    sig = get_processed_sig(sig)

    play_obj = sa.play_buffer(sig, 1, 2, SAMPLE_RATE)
    play_obj.wait_done()

# simulate_fan_sound(2)

# show_fan_sound_fft()


def show_fft_from_file(filename):
    sig = wav_to_array(filename)
    time_vec = time_vec_from_sig(sig)
    show_fft(sig, time_vec)

# show_fft_from_file("audio/ahhh.wav")

def triangle_wave(x):
    return np.abs(signal.sawtooth(x))
    

def recreate_file_waveform(filename, n_peaks, duration):
    sig = wav_to_array(filename)
    time_vec = time_vec_from_sig(sig)
    data : FFT_Data = get_fft(sig, time_vec)
    peaks = set()
    peak_indices = []
    for i in range(n_peaks):
        highest = (0, 0)
        highest_index = 0
        for j in range(len(data.amplitude)):
            if data.amplitude[j] > highest[1]:
                new = (data.sample_freq[j], data.amplitude[j])
                if new in peaks:
                    continue
                highest = new
                highest_index = j
        if highest == (0, 0):
            break
        peaks.add(highest)
        peak_indices.append(highest_index)
        


    time_vec = get_time_vec(duration)
    waves = []
    for i in peak_indices:
        waves.append(get_wave(data.sample_freq[i], 
                              data.amplitude[i], 
                              get_time_vec(duration, True), 
                              func=np.sin,
                              angle=data.angle[i]))
    processed = get_processed_sig(sum(waves))
    return processed
    
def time_of_fft(filename):
    sig = wav_to_array(filename)
    tv = time_vec_from_sig(sig)
    print("sample length: " + tv.size/SAMPLE_RATE)
    t1 = time.perf_counter()
    get_fft(sig, tv)
    t2 = time.perf_counter()
    print(f"time: {t2-t1}\tfreq: {1/(t2-t1)}")

w = recreate_file_waveform("proto/fft-sandbox/audio/ahhh.wav", 100, 5)
f = get_fft(w, time_vec_from_sig(w))
print(f.sample_freq.size)
plt.figure()
plt.plot(time_vec_from_sig(w), w)
plt.show()
play_obj = sa.play_buffer(w, 1, 2, SAMPLE_RATE)
play_obj.wait_done()