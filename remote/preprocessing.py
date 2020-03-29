import cv2
import numpy as np


def process_video(video, length=600, width=320, height=240):
    """
    Performs the preprocessing required for the video.
    
    video: cv2.VideoCapture instance with the video
    length: number of frames to take from the cv2.VideoCapture
    width: width of the resized video
    height: height of the resized video
    
    Returns:
    
    np.array of shape (length, height, width, 3)
    """
    frames = np.zeros((length, height, width, 3), dtype=np.uint8)
    for i in range(length):
        _, frame = video.read()
        frame = cv2.resize(frame, (width, height))
        frames[i] = frame
    video.release()
    cv2.destroyAllWindows()
    return frames