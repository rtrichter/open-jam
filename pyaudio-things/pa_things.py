import wave
import pyaudio
from dataclasses import dataclass
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from collections import deque

CHUNK = 1024
CHUNK_PER_FFT = 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 20

filename = "out/1.wav"

def time_vec_from_sig(sig, sample_rate=RATE):
    return np.linspace(0, sig.size/sample_rate, sig.size)

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

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []


# def live_fft():
#     fig = plt.figure()
#     ax1 = fig.add_subplot(1,1,1)

#     def animate(i):
#         xs = []
#         ys = []
#         for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#             data = stream.read(CHUNK)
#             array = np.frombuffer(data, dtype=np.int16)
#             fft = get_fft(array, time_vec_from_sig(array))
#             xs.append(i)
#             ys.append(fft.peak)
#         ax1.clear()
#         ax1.plot(xs, ys)
    
#     ani = animation.FuncAnimation(fig, animate, interval=93)
#     plt.show()

def live_fft():
    # must be recording FIRST (using stream name)
    # this should be refactored to not rely on outside variables asap
    print("live ffting")
    plt.ion() 
    fig = plt.figure()
    ax = fig.add_subplot(111)  
    q = deque()
    for i in range(CHUNK_PER_FFT):
        data = stream.read(CHUNK)
        array = np.frombuffer(data, dtype=np.int16)
        q.append(array)
    sig = np.concatenate([*q])
    fft = get_fft(sig, time_vec_from_sig(sig))
    line1, = ax.plot(fft.sample_freq, fft.amplitude, 'r-')
    ax.set(xlim=(0, 1000), ylim=(0, 10**8))
    
        
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS - 1)):
    while True:
        data = stream.read(CHUNK)
        array = np.frombuffer(data, dtype=np.int16)
        q.append(array)
        while len(q) > CHUNK_PER_FFT:
            q.popleft()
        sig = np.concatenate([*q])
        fft = get_fft(sig, time_vec_from_sig(sig))
        ax.set(ylim=(0, max(fft.amplitude)))
        line1.set_ydata(fft.amplitude)
        fig.canvas.draw()
        fig.canvas.flush_events()

live_fft()
    

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     x = np.frombuffer(data, dtype=np.int16)
#     print(x, type(x))
#     fft = get_fft(x, time_vec_from_sig(x))
#     plt.plot(fft.sample_freq, fft.amplitude)
#     plt.show()
#     frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
