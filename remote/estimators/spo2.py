import numpy as np
from ..utils.quality import crop_recording_errors


class SpO2Estimator:

    def __init__(self, A=100, B=5, area=90):
        self.A = A
        self.B = B
        self.area = area

    def estimate(self, video):
        frames = crop_recording_errors(video.frames)
        red_means = frames[:, :, :, video.channel_map['r']].reshape(len(frames), -1).mean(axis=1)
        blue_means = frames[:, :, :, video.channel_map['b']].reshape(len(frames), -1).mean(axis=1)
        red_stds = frames[:, :, :, video.channel_map['r']].reshape(len(frames), -1).std(axis=1)
        blue_stds = frames[:, :, :, video.channel_map['b']].reshape(len(frames), -1).std(axis=1)
        spo2 = self.A - self.B * ((red_stds / red_means) / (blue_stds / blue_means))
        spo2 = spo2[~np.isnan(spo2)]
        significance = (100-self.area)/2
        lower_bound = np.percentile(spo2, significance)
        upper_bound = np.percentile(spo2, self.area + significance)
        clipped_spo2 = spo2[(spo2 > lower_bound) & (spo2 < upper_bound)]
        is_valid = True
        return np.mean(clipped_spo2), is_valid