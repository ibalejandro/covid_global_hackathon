import cv2
from .reading import cv2_to_numpy


class VideoReader:
    pass



class NumpyVideo(VideoReader):

    def __init__(self, path):
        video = cv2.VideoCapture(path)
        self._frames = cv2_to_numpy(video)
        self._format = ('frame', 'width', 'height', 'channel')
        self._channel_map = {'b': 0, 'g': 1, 'r': 2}
        self._fps = video.get(cv2.CAP_PROP_FPS)

    @property
    def frames(self):
        return self._frames

    @property
    def format(self):
        return self._format

    @property
    def channel_map(self):
        return self._channel_map

    @property
    def fps(self):
        return self._fps
