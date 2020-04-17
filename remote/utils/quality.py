from scipy import signal


def crop_recording_errors(frames, crop_from_start=120, crop_from_end=120):
    return frames[crop_from_start:-crop_from_end]


def butterworth_filter_signal(s, fps, order=2, bandpass_range=(0.8, 3)):
    low = bandpass_range[0]/(fps/2)
    upp = bandpass_range[1]/(fps/2)
    b, a = signal.butter(order, [low, upp], 'bandpass')
    return signal.filtfilt(b, a, s)
