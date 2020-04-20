import scipy
import numpy as np
import pandas as pd
from ..utils.assertions import validate_channel_map
from ..utils import intersect2d, degree_to_rad, coordinate_grid
from .base_classes import Estimator


class ParaboloidHRE(Estimator):
    """
    The Kurylyak heart rate estimation algorithm requires a calibration step.
    """

    def __repr__(self):
        return f'Paraboloid with {self.roi_detector}'

    def __init__(self, roi_detector):
        super().__init__(roi_detector)

    def map_frame(self, frame, roi, video):
        if roi.sum() == 0:
            return np.nan
        frame = frame[:, :, video.channel_map['r']]
        w, h = frame.shape
        frame_idxs = coordinate_grid(h, w)
        roi = frame_idxs[roi]
        x_min, x_max = roi[:, 1].min(), roi[:, 1].max()
        y_min, y_max = roi[:, 0].min(), roi[:, 0].max()
        cx = np.mean(roi[:, 1], dtype=np.int)
        cy = np.mean(roi[:, 0], dtype=np.int)
        centroid = np.array([cy, cx])

        radii = []
        for angle in (0, 45, 90, 135, 180, 225, 270, 315):
            if angle == 90:
                points_along_direction = np.array([(y, cx) for y in range(y_min, cy + 1)], dtype=np.int64)
            elif angle == 270:
                points_along_direction = np.array([(y, cx) for y in range(cy, y_max + 1)], dtype=np.int64)
            elif angle < 90 or angle > 270:
                points_along_direction = np.array([((x - cx) * np.tan(degree_to_rad(-angle)) + cy, x) 
                                                for x in range(cx, x_max + 1)], dtype=np.int64)
            else:
                points_along_direction = np.array([((x - x_min) * np.tan(degree_to_rad(angle)) + cy, cx - (x - x_min)) 
                                                for x in range(x_min, cx + 1)], dtype=np.int64)
            roi = np.insert(roi, 0, centroid, axis=0)
            intersections = intersect2d(roi, points_along_direction)

            if angle == 90:
                intersection_point = intersections[np.argmin(intersections[:, 0])]
            elif angle == 270:
                intersection_point = intersections[np.argmax(intersections[:, 0])]
            elif angle < 90 or angle > 270:
                intersection_point = intersections[np.argmax(intersections[:, 1])]
            else:
                intersection_point = intersections[np.argmin(intersections[:, 1])]

            if intersection_point[0] in (0, h) or intersection_point[1] in (0, w):
                continue
            distance_from_centroid_to_intersection = np.sqrt(np.sum(np.square(intersection_point - centroid)))
            radii.append(distance_from_centroid_to_intersection)
        return -np.mean(radii) #this seems to assume the mode is transmission

    def reduce_values(self, values, video):
        values = pd.Series(values).interpolate('quadratic').values
        freqs = scipy.fft.rfft(values)[1:]
        dominant_frequency = np.argmax(freqs)
        bpm = 60 * dominant_frequency / video.fps
        return bpm


class OptimizedParaboloidHRE(Estimator):
    """
    The Kurylyak heart rate estimation algorithm requires a calibration step.
    """

    def __repr__(self):
        return f'Paraboloid with {self.roi_detector}'

    def __init__(self, roi_detector):
        super().__init__(roi_detector)

    def map_frame(self, frame, roi, video):
        if roi.sum() == 0:
            return np.nan
        frame = frame[:, :, video.channel_map['r']]
        w, h = frame.shape
        frame_idxs = coordinate_grid(h, w)
        roi = frame_idxs[roi]
        cx = np.mean(roi[:, 1], dtype=np.int)
        cy = np.mean(roi[:, 0], dtype=np.int)
        centroid = np.array([cy, cx])
        roi = np.insert(roi, 0, centroid, axis=0)
        x_min, x_max = roi[:, 1].min(), roi[:, 1].max()
        y_min, y_max = roi[:, 0].min(), roi[:, 0].max()

        t = np.arctan2(roi[:, 0] - cy, roi[:, 1] - cx)

        radii = []
        for angle in (0, 45, 90, 135, 180, 225, 270, 315):
            intersections = roi[np.abs(t - degree_to_rad(angle)) < 1e-4]
            if intersections.sum() == 0:
                continue

            if angle == 90:
                intersection_point = intersections[np.argmin(intersections[:, 0])]
            elif angle == 270:
                intersection_point = intersections[np.argmax(intersections[:, 0])]
            elif angle < 90 or angle > 270:
                intersection_point = intersections[np.argmax(intersections[:, 1])]
            else:
                intersection_point = intersections[np.argmin(intersections[:, 1])]

            if intersection_point[0] in (0, h) or intersection_point[1] in (0, w):
                continue
            distance_from_centroid_to_intersection = np.sqrt(np.sum(np.square(intersection_point - centroid)))
            radii.append(distance_from_centroid_to_intersection)
        return -np.mean(radii) #this seems to assume the mode is transmission

    def reduce_values(self, values, video):
        values = pd.Series(values).interpolate('quadratic').values
        freqs = scipy.fft.rfft(values)[1:]
        dominant_frequency = np.argmax(freqs)
        bpm = 60 * dominant_frequency / video.fps
        return bpm


class AverageHRE(Estimator):

    def __repr__(self):
        return f'Average with {self.roi_detector}'
    
    def __init__(self, roi_detector):
        super().__init__(roi_detector)

    def map_frame(self, frame, roi, video):
        if roi.sum() == 0:
            return np.nan
        return -np.mean(frame[:, :, video.channel_map['r']][roi]) #assumes transmission mode

    def reduce_values(self, values, video):
        values = pd.Series(values).interpolate('quadratic').values
        freqs = scipy.fft.rfft(values)[1:]
        dominant_frequency = np.argmax(freqs)
        bpm = 60 * dominant_frequency / video.fps
        return bpm
