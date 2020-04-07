def validate_channel_map(channel_map):
    if set(channel_map.keys()) != set(['r', 'g', 'b']):
        raise ValueError("Channel map must contain keys ['r', 'g', 'b']")
    if set(channel_map.values()) != set([0, 1, 2]):
        raise ValueError("Channel map must contains index values (0, 1, 2)")