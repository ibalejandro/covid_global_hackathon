import cv2
import numpy as np


def cv2_to_numpy(video, resize_to):
    frames = []
    while True:
        _, frame = video.read()
        if frame is None:
            break
        frames.append(cv2.resize(frame, resize_to))
    return np.array(frames, dtype=np.uint8)
