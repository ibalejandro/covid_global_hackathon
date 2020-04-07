def trim_limits(video, frame_validity):
    """
    Trims invalid frames from start and end of video.

    Parameters:
    -----------
    * video: numpy array of shape (timesteps, height, width, channels)
    * frame_validity: boolean array of shape (timesteps, ) where True indicates the frame
                      is valid, and False otherwise.
    """
    return video


def interpolate_frames(video, frame_validity, max_interpolation_length):
    """
    Interpolates invalid frames within the video.

    Parameters:
    -----------
    * interpolate: bool, whether or not to interpolate invalid frames within the video.
    * max_interpolation_length: maximum length (in frames) to interpolate between, raises
                                an exception if the amount of consecutive invalid frames is larger than
                                this value.
    """
    return video