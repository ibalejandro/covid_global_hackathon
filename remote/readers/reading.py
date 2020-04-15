import numpy as np


def cv2_to_numpy(video):
    frames = []
    while True:
        _, frame = video.read()
        if frame is None:
            break
        frames.append(frame)
    return np.array(frames, dtype=np.uint8)
