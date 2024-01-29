import config

def sec2sample(seconds: int) -> int:
    # forces to int since you can't have a partial sample
    # truncation should avoid potential index errors
    return int(seconds * config.RATE)

def sample2sec(samples: int) -> float:
    return samples / config.RATE