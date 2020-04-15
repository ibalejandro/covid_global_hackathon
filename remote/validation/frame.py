import numpy as np
from ..utils.assertions import validate_channel_map
from abc import ABCMeta, abstractmethod


class FrameValidator(metaclass=ABCMeta):

    def __init__(self, channel_map):
        validate_channel_map(channel_map)
        self.channel_map = channel_map

    @abstractmethod
    def validate(self, frame):
        raise NotImplementedError('Override on inheritance')


class ColorDistributionFrameValidator(FrameValidator):
    """
    The validation algorithms presented here are based on Chapter 5 (Smartphone-based
    Photoplethysmography Measurement) by Yuriy Kurylyak, Francesco Lamonaca and Domenico Grimaldi
    of the book "Digital Image and Signal Processing for Measurement Systems".
    """

    @classmethod
    def __repr__(cls):
        return 'ColorDistribution'

    def __init__(self, channel_map, **kwargs):
        super().__init__(channel_map)
        self.gled_min = kwargs.get('gled_min', 10)
        self.rled_min = kwargs.get('rled_min', 128)
        self.g_max = kwargs.get('g_max', 128)
        self.b_max = kwargs.get('b_max', 128)
        self.s_max = kwargs.get('s_max', 40)
        self.gnoled_max = kwargs.get('gnoled_max', 10)
        self.rnoled_min = kwargs.get('rnoled_min', 10)

    def _is_led(self, frame):
        """Detects if a frame is taken with a LED light.

        Arguments:
            frame: numpy array of shape (height, width, number_of_channels)

        Returns:
            boolean -- True if the frame was taken with a LED light, False otherwise.
        """
        return np.mean(frame[:, :, self.channel_map.get('g')]) >= self.gled_min

    def _is_valid_led_frame(self, frame):
        """
        Performs the following validation to assert the frame is adequate:

        1. Amount of green must not be very small
        2. Amount of red should be mostly high
        3. Amount of green should be mostly low
        4. Amount of blue should be mostly low
        5. Values for each channel should not be distributed too much
        """
        r = self.channel_map.get('r')
        g = self.channel_map.get('g')
        b = self.channel_map.get('b')

        m_r, m_g, m_b = np.mean(frame[:, :, r]), np.mean(frame[:, :, g]), np.mean(frame[:, :, b])
        s_r, s_g, s_b = np.std(frame[:, :, r]), np.std(frame[:, :, g]), np.std(frame[:, :, b])

        result = [True]
        log = []
        if not m_g - s_g >= self.gled_min:
            result.append(False)
            log.append(f'LED - NOT ENOUGH GREEN ({m_g - s_g}/{self.gled_min})')
        if not m_r - s_r >= self.rled_min:
            result.append(False)
            log.append(f'LED - NOT ENOUGH RED ({m_r - s_r}/{self.rled_min})')
        if not m_g + s_g <= self.g_max:
            result.append(False)
            log.append(f'LED - TOO MUCH GREEN ({m_g + s_g}/{self.g_max})')
        if not m_b + s_b <= self.b_max:
            result.append(False)
            log.append(f'LED - TOO MUCH BLUE ({m_b + s_b}/{self.b_max})')
        if not max(s_r, s_g, s_b) <= self.s_max:
            result.append(False)
            log.append(f'LED - TOO MUCH VARIANCE (R:{s_r}, G:{s_g}, B:{s_b}/{self.s_max})')

        if len(log) == 0:
            log.append('LED - VALID')
        
        return all(result), ' & '.join(log)

    def _is_valid_no_led_frame(self, frame):
        """
        Performs the following validation to assert the frame is adequate:

        1. Amount of green must be very small
        2. Amount of blue should be mostly low
        3. Amount of red must not be small
        4. Values for each channel should not be distributed too much
        """
        r = self.channel_map.get('r')
        g = self.channel_map.get('g')
        b = self.channel_map.get('b')

        m_r, m_g, m_b = np.mean(frame[:, :, r]), np.mean(frame[:, :, g]), np.mean(frame[:, :, b])
        s_r, s_g, s_b = np.std(frame[:, :, r]), np.std(frame[:, :, g]), np.std(frame[:, :, b])

        result = [True]
        log = []
        if not m_g + s_g < self.gnoled_max:
            result.append(False)
            log.append(f'NO LED - TOO MUCH GREEN ({m_g + s_g}/{self.g_max})')
        if not m_b + s_b < self.b_max:
            result.append(False)
            log.append(f'NO LED - TOO MUCH BLUE ({m_b + s_b}/{self.b_max})')
        if not m_r > self.rnoled_min:
            result.append(False)
            log.append(f'NO LED - NOT ENOUGH RED ({m_r - s_r}/{self.rled_min})')
        if not max(s_r, s_g, s_b) <= self.s_max:
            result.append(False)
            log.append(f'LED - TOO MUCH VARIANCE (R:{s_r}, G:{s_g}, B:{s_b}/{self.s_max})')
        
        if len(log) == 0:
            log.append('LED - VALID')
        
        return all(result), ' & '.join(log)
        
    def validate(self, frame):
        """Validates if a frame has the requirements according to Kurylyak validation.
        
        Arguments:
            frame {numpy array of shape (dim1, dim2, 3)} -- the frame to validate.
        
        Returns:
            boolean -- True if the frame is valid.
            str -- log with the causes of the frame invalidation.
        """
        if self._is_led(frame):
            return self._is_valid_led_frame(frame)
        else:
            return self._is_valid_no_led_frame(frame)
