import numpy as np
import tensorflow as tf


def conv_2d(frames, kernel):
    n, h, w = frames.shape
    kh, kw = kernel.shape
    frames = frames.reshape((n, h, w, 1)).astype(np.float32)
    kernel = kernel.reshape(kh, kw, 1, 1)
    convs = tf.keras.backend.conv2d(frames, kernel=kernel).numpy().reshape((n, h - kh + 1, w - kw + 1))
    tf.keras.backend.clear_session()
    return convs
