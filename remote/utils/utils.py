import numpy as np


def intersect2d(A, B):
    nrows, ncols = A.shape
    dtype={'names':['f{}'.format(i) for i in range(ncols)],
           'formats':ncols * [A.dtype]}
    C = np.intersect1d(A.view(dtype), B.view(dtype))
    return C.view(A.dtype).reshape(-1, ncols)


def degree_to_rad(angle):
    return angle * np.pi / 180


def coordinate_grid(max_x, max_y):
    return np.array([[(y, x) for x in range(max_x)] for y in range(max_y)])


def function_per_frame(video, channel, function):
    raise DeprecationWarning()
    reshaped_video = video[:, :, :, channel].reshape(video.shape[0], -1)
    return function(reshaped_video, axis=-1)