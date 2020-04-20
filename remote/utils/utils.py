import numpy as np


def extract_frequency_in_bpm(s, fps):
    """Taken from:
    https://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python
    """
    w = np.abs(np.fft.fft(s))
    freqs = np.fft.fftfreq(len(w))
    idx = np.argmax(w)
    dominant_freq = freqs[idx]
    return 60*np.abs(dominant_freq * fps)