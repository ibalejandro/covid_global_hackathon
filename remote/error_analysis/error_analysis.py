import numpy as np
import matplotlib.pyplot as plt


def show_region_of_interest(frame, roi):
    """[summary]
    
    Arguments:
        frame {[np.array of shape (w, h)]} -- [description]
        roi {[np.array of shape (n, 2)]} -- [n is the number of pixels in the ROI. 
                                             The 2 values are for (y, x) coordinates]
    """
    plt.clf()
    masked_frame = np.zeros_like(frame, dtype=np.uint8)
    masked_frame[roi[:, 0], roi[:, 1]] = 255
    plt.imshow(masked_frame)

def show_validity_map(bool_array):
    pass

def show_fourier_spectrum(signal, frequency_range=(20, 75)):
    low, upp = frequency_range
    coefs = np.abs(np.fft.rfft(signal)[low:upp])
    plt.clf()
    plt.plot(coefs)
    plt.xticks([i for i in range(0, len(coefs), 10)], labels=[i for i in range(low, upp, 10)])

def main_detected_frequencies(signal, frequency_range=(20, 75), stds=2):
    low, upp = frequency_range
    coefs = np.abs(np.fft.rfft(signal)[low:upp])
    main_coefs = coefs[coefs > np.mean(coefs) + stds * np.std(coefs)]
    