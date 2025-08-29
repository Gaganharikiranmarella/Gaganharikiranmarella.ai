def clamp(value, min_value, max_value):
    """Clamp value between min_value and max_value."""
    return max(min_value, min(value, max_value))

def flatten_2d_list(lst):
    """Flatten a 2D list into a 1D list."""
    return [item for sublist in lst for item in sublist]
