import numpy as np
import matplotlib.pyplot as plt


def show_region_of_interest(frame, roi):
    """[summary]
    
    Arguments:
        frame {[np.array of shape (w, h)]} -- [description]
        roi {[np.array of shape (n, 2)]} -- [n is the number of pixels in the ROI. 
                                             The 2 values are for (y, x) coordinates]
    """
    plt.clf()
    masked_frame = np.zeros_like(frame, dtype=np.uint8)
    masked_frame[roi[:, 0], roi[:, 1]] = 255
    plt.imshow(masked_frame)

def show_validity_map(bool_array):
    pass