import numpy as np
from .base_classes import Estimator


class LinearSpO2Estimator(Estimator):

    def __repr__(self):
        return f'Linear with {self.roi_detector}'
    
    def __init__(self, roi_detector, A=100, B=5, area=90):
        super().__init__(roi_detector)
        self.A = A
        self.B = B
        self.area = area

    def map_frame(self, frame, roi, video):
        if roi.sum() == 0:
            return np.nan
        m_r = np.mean(frame[:, :, video.channel_map['r']][roi])
        m_b = np.mean(frame[:, :, video.channel_map['b']][roi])
        s_r = np.std(frame[:, :, video.channel_map['r']][roi])
        s_b = np.std(frame[:, :, video.channel_map['b']][roi])
        spo2 = self.A - self.B * ((s_r / m_r) / (s_b / m_b))
        return spo2

    def reduce_values(self, values, video):
        values = values[~np.isnan(values)]
        significance = (100-self.area)/2
        lower_bound = np.percentile(values, significance)
        upper_bound = np.percentile(values, self.area + significance)
        clipped_values = values[(values >= lower_bound) & (values <= upper_bound)]
        return np.mean(clipped_values)
