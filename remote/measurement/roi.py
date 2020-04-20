import numpy as np
from .base_classes import ROI
    

class RedThresholdROI(ROI):

    def __repr__(self):
        return 'RedThreshold'
    
    def __init__(self, calibration_frames=180, theta=0.2):
        self.calibration_frames = calibration_frames
        self.theta = theta
        self.is_fit = False

    def fit(self, video):
        """Fits the required parameters on the video. Used for calibration.
        
        Arguments:
            video {VideoReader} -- video
        """
        thresholds = np.zeros(shape=(self.calibration_frames,))
        for i in range(self.calibration_frames):
            thresholds[i] = np.percentile(video.frames[i, :, :, video.channel_map['r']].flatten(), int(100*(1-self.theta)))
        self.threshold = np.mean(thresholds)
        self.is_fit = True
        return self

    def transform(self, video):
        """Returns the boolean mask containing the RoI for each frame in the video.
        
        Arguments:
            video {VideoReader} -- video
        
        Returns:
            [numpy array] -- boolean mask with the RoI for each frame.
        """
        if not self.is_fit:
            raise ValueError('Call .fit method before .transform')
        return video.frames[:, :, :, video.channel_map['r']] > self.threshold


class FullChannelROI(ROI):

    def __repr__(self):
        return 'Full Channel'

    def __init__(self, channel):
        assert channel in ('r', 'g', 'b')
        self.channel = channel

    def fit(self, video):
        return self

    def transform(self, video):
        return np.ones_like(video.frames[:, :, :, video.channel_map[self.channel]], dtype=np.bool)
