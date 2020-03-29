def function_per_frame(video, channel, function):
    reshaped_video = video[:, :, :, channel].reshape(video.shape[0], -1)
    return function(reshaped_video, axis=-1)