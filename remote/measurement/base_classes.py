import numpy as np
from abc import ABCMeta, abstractmethod


class ROI(metaclass=ABCMeta):

    @abstractmethod
    def fit(self, video):
        raise NotImplementedError('Override on inheritance')

    @abstractmethod
    def transform(self, video):
        raise NotImplementedError('Override on inheritance')


class Estimator(metaclass=ABCMeta):

    def __init__(self, roi_detector):
        assert isinstance(roi_detector, ROI)
        self.roi_detector = roi_detector

    def fit(self, video):
        self.roi_detector.fit(video)
        return self

    def measure(self, video, reduce=True):
        self.fit(video)
        rois = self.roi_detector.transform(video)
        values = []
        for i, frame in enumerate(video.frames):
            values.append(self.map_frame(frame, rois[i], video))
        values = np.array(values)
        if not reduce:
            return values
        return self.reduce_values(values, video)

    @abstractmethod
    def map_frame(self, frame, roi, video):
        raise NotImplementedError('Override on inheritance')

    @abstractmethod
    def reduce_values(self, values, video):
        raise NotImplementedError('Override on inheritance')
