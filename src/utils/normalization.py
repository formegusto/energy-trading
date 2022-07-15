def min_max_normalization(data):
    return (data - data.min()) / (data.max() - data.min())
