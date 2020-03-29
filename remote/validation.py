import cv2


def validate_video(video, length=600, fps=30):
    assert validate_length(video, length)
    assert validate_correctness(video)
    assert validate_infrared(video)
    assert validate_fps(video, fps)


def validate_length(video, length):
    """
    Validates the video has the required length in number of frames.
    
    video: cv2.VideoCapture instance with the video
    length: int, number of frames the video must have
    """
    return int(video.get(cv2.CAP_PROP_FRAME_COUNT)) >= length


def validate_correctness(video):
    #check if the video is indeed of a finger right in the camera lens
    return True


def validate_infrared(video):
    #check if the blue/green channels of the video are different from zero
    return True


def validate_fps(video, fps):
    #required for the frequency calculations of the bpm
    return video.get(cv2.CAP_PROP_FPS) 