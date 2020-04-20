import numpy as np
import tensorflow as tf


def conv_2d(frames, kernel):
    n, h, w = frames.shape
    kh, kw = kernel.shape
    frames = frames.reshape((n, h, w, 1)).astype(np.float32)
    kernel = kernel.reshape(kh, kw, 1, 1)
    conv_op = tf.keras.layers.Conv2D(filters=1, kernel_size=(kh, kw), use_bias=False, input_shape=(h, w, 1),
                                     kernel_initializer=tf.keras.initializers.Constant(kernel))
    return conv_op(frames).numpy().reshape((n, h - kh + 1, w - kw + 1))
