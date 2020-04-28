import numpy as np
from ..utils.quality import crop_recording_errors, butterworth_filter_signal
from ..utils.utils import extract_frequency_in_bpm
from ..roi import TemporalDifferenceROI


class HeartRateEstimator:

    def __init__(self):
        self.roi_generator = TemporalDifferenceROI()

    def _generate_signal(self, frames, roi, channel):
        s = np.zeros(len(roi))
        frames = frames[:, :, :, channel]
        for i, r in enumerate(roi):
            s[i] = frames[i, r].mean()
        return s

    def _check_validity(self, s, threshold=20):
        freqs = np.abs(np.fft.rfft(s))
        mean_amplitude = np.mean(freqs[freqs > 0])
        return mean_amplitude < threshold

    def estimate(self, video, return_signals=False):
        raw_signal = video.frames[:, :, :, video.channel_map['r']].reshape(len(video.frames), -1).mean(axis=-1)
        frames = crop_recording_errors(video.frames)
        cropped_signal = frames[:, :, :, video.channel_map['r']].reshape(len(frames), -1).mean(axis=-1)
        # roi = self.roi_generator.get_roi(frames, video.fps)
        roi = np.ones_like(frames[:, :, :, 0]).astype(np.bool)
        roi_signal = self._generate_signal(frames, roi, video.channel_map['r'])
        filtered_signal = butterworth_filter_signal(roi_signal, video.fps)
        is_valid = self._check_validity(filtered_signal)
        bpm = extract_frequency_in_bpm(filtered_signal, video.fps)
        if return_signals:
            return bpm, raw_signal, cropped_signal, roi_signal, filtered_signal
        return bpm, is_valid