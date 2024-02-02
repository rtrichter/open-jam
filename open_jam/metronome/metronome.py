# from config import *
from fractions import Fraction

MAX_VOLUME = 10

class Tempo:

    __slots__ = ["__beat_length", "__bpm"]

    def __init__(self, beat_length: tuple[int], bpm: int = None):
        self.__beat_length = beat_length
        self.__bpm = bpm
    
    @property
    def beat_length(self) -> tuple[int]:
        return self.__beat_length
    
    @property
    def bpm(self) -> int:
        return self.__bpm
    
    def inc_bpm(self, increment: int):
        self.__bpm += increment
    
    def __str__(self):
        return f"{self.beat_length[0]}/{self.beat_length[1]}={self.bpm}"
    def __eq__(self, other):
        if type(self) != type(other):
            raise ValueError(f"Incompatible types: {type(self)} == {type(other)}")
        return self.__slots__ == other.__slots__
    def __repr__(self):
        return str(self)


class TimeSig:
    
    __slots__ = ["__top", "__bottom"]

    def __init__(self, top: int, bottom: int):
        self.__top = top
        self.__bottom = bottom

    @property
    def top(self) -> int:
        return self.__top
    
    @property
    def bottom(self) -> int:
        return self.__bottom

    def __str__(self):
        return f"{self.top}/{self.bottom}"
    def __eq__(self, other):
        if type(self) != type(other):
            raise ValueError(f"Incompatible types: {type(self)} == {type(other)}")
        return self.__slots__ == other.__slots__
    def __repr__(self):
        return str(self)

# class EmphasisPattern:
    
#     __slots__ = ["__n_beats", "__pattern"]

#     def __init__(self, n_beats: int, pattern: list[int] = None):
#         self.__n_beats = n_beats if n_beats else 4
#         if pattern is None:
#             self.__pattern = pattern
#         else:
#             pattern = [MAX_VOLUME//2 for _ in range(self.__n_beats)]
    
#     @property
#     def time_sig(self) -> TimeSig:
#         return self.__time_sig

#     @property
#     def pattern(self) -> list[int]:
#         return self.__pattern



class Metronome:
    
    __slots__ = ["__tempo", "__time_sig", "__emphasis"]

    def __init__(
            self,
            tempo: Tempo,
            time_sig: TimeSig = None,
            emphasis: list[int] = None):
        self.__tempo = tempo
        self.__time_sig = TimeSig(4, 4) if time_sig is None else time_sig
        if emphasis is None:
            self.__emphasis = [MAX_VOLUME//2 for _ in range(self.__time_sig.top)]
        else:
            # make sure that pattern matches the time sig
            if len(emphasis) != self.__time_sig.top:
                raise ValueError(
                    f"""pattern of length {len(emphasis)}"""
                    + f""" does not match time signature {self.__time_sig}""")
            # only if they do match
            self.__emphasis = emphasis

    @property
    def tempo(self) -> Tempo:
        return self.__tempo
    
    @property
    def time_sig(self) -> TimeSig:
        return self.__time_sig
    
    @property
    def emphasis(self) -> list[int]:
        return self.__emphasis
    
    def inc_tempo(self, increment: int) -> None:
        self.tempo.inc_bpm(increment)

    def set_beat_volume(self, beat, volume) -> None:
        # make sure volume does not exceed maximum
        #TODO log a warning that volume was clipped
        if volume > MAX_VOLUME:
            volume = MAX_VOLUME
        if volume < 0:
            volume = 0

        # make sure the beat is inside our measure
        if beat >= len(self.pattern):
            raise ValueError(f"beat ({beat}) exceeds the {len(self.pattern)} beat pattern")
        self.pattern[beat] = volume

    def __eq__(self, other):
        if type(self) != type(other):
            raise ValueError(f"Incompatible types: {type(self)} == {type(other)}")
        return self.__slots__ == other.__slots__