import numpy as np
from ..utils.math import conv_2d


class TemporalDifferenceROI:

    def __init__(self, kernel_size=(50, 50)):
        self.kernel_size = kernel_size

    def _denoised_temporal_difference(self, frames, fps, denoising_length=3):
        frame_difference = np.abs(frames[:-1] - frames[1:])
        cumulative_frame_difference = frame_difference.cumsum(axis=0)
        frames_to_accum = int(fps * denoising_length)
        return np.array([cumulative_frame_difference[i + frames_to_accum] - cumulative_frame_difference[i] \
                        for i in range(len(cumulative_frame_difference) - frames_to_accum)])

    def get_roi(self, frames, fps):
        assert len(frames.shape) == 4
        frames = frames.mean(axis=-1)
        roi = np.zeros_like(frames)
        td = self._denoised_temporal_difference(frames, fps)
        kernel = np.ones(self.kernel_size) * (1 / (np.prod(self.kernel_size)))
        convs = conv_2d(td, kernel)
        argmaxes = convs.reshape(len(convs), -1).argmax(axis=1)
        argmax_coords = np.array([(a // convs.shape[-1], a % convs.shape[-1]) for a in argmaxes])
        for i, (y, x) in enumerate(argmax_coords):
            roi[i, y:y+self.kernel_size[0], x:x+self.kernel_size[1]] = 1
        roi = roi.astype(np.bool)
        return roi[:i+1]