def fix_with_trimming(frames, bool_array):
    new_start_index = 0
    new_end_index = len(frames) + 1
    i = 0
    while not bool_array[i]:
        new_start_index += 1
        i += 1
    i = -1
    while not bool_array[i]:
        new_end_index -= 1
        i -= 1
    return frames[new_start_index : new_end_index]


def fix_with_interpolation(frames, bool_array):
    raise NotImplementedError()