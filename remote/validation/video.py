from ..readers import VideoReader
from ..utils.video_fixing import interpolate_frames, trim_limits
from .fixing import fix_with_trimming, fix_with_interpolation


class VideoValidator:

    def __init__(self, frame_validator):
        self.frame_validator = frame_validator

    def validate(self, video):
        """Validates the status of each frame of the video according to the logic implemented
        in `self.frame_validator`
        
        Arguments:
            video {VideoReader} -- video to validate

        Returns:
            boolean -- True if all the frames are valid
            dict -- dictionary with keys {'result', 'log'}, showing True for each correct
                    frame, and the respective log information for further analysis.
        """
        assert isinstance(video, VideoReader)
        results = {'result': [], 'log': []}
        for frame in video.frames:
            res, log = self.frame_validator.validate(frame)
            results['result'].append(res)
            results['log'].append(log)
        all_valid = all(results['result'])
        return all_valid, results

    def fix_video(self, video, bool_array, trim=True, interpolate=True, min_length=600, max_interpolation_length=15):
        """
        Attempts to fix the video.

        Parameters:
        -----------
            video {VideoReader}
            bool_array {iterable} -- of shape (timesteps) where True indicates the frame is valid.
            trim {bool} -- whether or not to drop invalid frames at start and end of video.
            interpolate {bool} -- whether or not to interpolate invalid frames within the video.
            min_length {int} -- minimum length (in frames) to make the video viable, raises an exception
                                if the trimmed video doesn't contain at least this length.
            max_interpolation_length {int} -- maximum length (in frames) to interpolate between, raises
                                              an exception if the amount of consecutive invalid frames is 
                                              larger than this value.
        """
        if trim:
            fixed_frames = fix_with_trimming(video.frames, bool_array)
            if len(fixed_frames) < min_length:
                raise ValueError("Trimming invalid, not enough valid frames.")
            video.frames = fixed_frames
        return video
