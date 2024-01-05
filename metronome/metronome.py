import globals as G
from fractions import Fraction
import simpleaudio as sa
from threading import Thread
import time

class Metronome:
    """
    sound (str): path to the file containing the metronome's sound
    tempo (Fraction, float): tempo for the metronome to run during playback
        units: bpm (beats per minute)
    signature ((int, int)): time signature (4 over 4 = (4, 4))
    """
    __slots__ = ["__sound", "tempo", "signature", "__wave", "__thread", 
                 "__stop_thread", "__mute", "__beat", "__bar", "__mute_func"]

    def __init__(self, sound=G.DEFAULT_SOUND, tempo=G.DEFAULT_TEMPO, signature=G.DEFAULT_SIGNATURE, mute_func=lambda: False):
        self.__sound = sound
        self.tempo = tempo
        self.signature = signaturne
        self.__wave = sa.WaveObject.from_wave_file(sound)
        self.__thread = Thread(target=self._click_thread_func)
        self.__mute = False
        self.__beat = 1
        self.__bar = 1
        self.__mute_func = mute_func
    
    @property
    def bar(self):
        return self.__bar

    @property
    def beat(self):
        return self.__beat
    
    def _click_thread_func(self):
        while not self.__stop_thread:
            print(f"{self.__bar} | {self.__beat}")
            time.sleep(self.click_period)
            self.increment()
            if self.__mute:
                continue
            self.play_one_click()
    
    def start(self):
        self.__stop_thread = False
        self.__thread.start()
    
    def stop(self):
        self.__stop_thread = True
    
    def mute(self):
        self.__mute = True

    def unmute(self):
        self.__mute = False
        
    @property
    def click_period_frac(self):
        # Time between two clicks
        # print(f"60/{self.signature[1]}*{self.tempo[0]}*{self.tempo[1]}")
        return Fraction(60, self.signature[1] * self.tempo[0] * self.tempo[1])
    
    @property
    def click_period(self):
        return float(self.click_period_frac)

    def increment(self):
        self.__beat += 1
        if self.beat > self.signature[0]:
            self.__bar += 1
            self.__beat = 1
        self.__mute = self.__mute_func(self)

    
    def play_one_click(self):
        self.__wave.play()
       
def mute_every_other_bar(metronome): 
    return metronome.bar%2 == 1

if __name__ == "__main__":
    tempo = (Fraction(3, 8), 60)
    sig = (6, 8)
    metro = Metronome(tempo=tempo, signature=sig, mute_func=mute_every_other_bar) 
    print(f"T={metro.click_period_frac}")
    metro.start()
    # time.sleep(0.01)
    # time.sleep(1)
    # metro.mute()
    # time.sleep(1)
    # metro.unmute()
    # time.sleep(1)
    time.sleep(20)
    metro.stop()