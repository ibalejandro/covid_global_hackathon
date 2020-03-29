import numpy as np
from .utils import function_per_frame

def calculate_spO2(video, A=100, B=5, use_reduce=True, use_area=90):
    """
    Calculates the blood oxygen saturation.

    Algorithm based on the paper: 
    Determination of SpO2 and Heart-rate using Smartphone Camera, Kanva et al.
    https://www.iiitd.edu.in/noc/wp-content/uploads/2017/11/06959086.pdf

    video: numpy array
    A: hyperparameter used to adjust the data
    B: hyperparameter used to adjust the data
    use_reduce: if True returns a scalar, indicating the average SpO2 across the video frames
    use_area: when reducing, determines the distribution area to use to calculate the mean.
              used for robustness against outliers.
    """
    channels = {'b': 0, 'g': 1, 'r': 2}
    red_means = function_per_frame(video, channel=channels['r'], function=np.mean)
    blue_means = function_per_frame(video, channel=channels['b'], function=np.mean)
    red_stds = function_per_frame(video, channel=channels['r'], function=np.std)
    blue_stds = function_per_frame(video, channel=channels['b'], function=np.std)
    spo2 = A - B * ((red_stds / red_means) / (blue_stds / blue_means))
    if use_reduce:
        nans = np.isnan(spo2).sum()
        print(f'Found {nans} NaNs, removing them')
        spo2 = spo2[~np.isnan(spo2)]
        significance = (100-use_area)/2
        lower_bound = np.percentile(spo2, significance)
        upper_bound = np.percentile(spo2, use_area + significance)
        print(f'Calculating trimmed mean in the range ({lower_bound}, {upper_bound})')
        clipped_spo2 = spo2[(spo2 > lower_bound) & (spo2 < upper_bound)]
        print(f'Clipped SpO2 contains {len(clipped_spo2)} values')
        return np.mean(clipped_spo2)
    return spo2


def calculate_heart_rate(video, use_reduce=True, frequency_range=(20, 200), fps=30):
    channels = {'b': 0, 'g': 1, 'r': 2}
    lower_bound, upper_bound = frequency_range
    duration = video.shape[0] / 30
    red_means = function_per_frame(video, channel=channels['r'], function=np.mean)
    if use_reduce:
        fourier_coefs = abs(np.fft.fft(red_means)[lower_bound:upper_bound + 1])
        dominant_frequency = np.argmax(fourier_coefs) + lower_bound
        heart_rate = dominant_frequency * 60 / duration
        return heart_rate
    return red_means


def discretize_spO2(spo2):
    if spo2 >= 90:
        return 'normal'
    elif spo2 >= 80:
        return 'low'
    else:
        return 'dangerously low'


def discretize_heart_rate(bpm, age, sex, fitness_level):
    pass