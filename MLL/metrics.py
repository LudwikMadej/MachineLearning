import numpy as np

def euclidean(x, y, weights=None, axis=None):
    z = np.power(x - y, 2)
    if weights:
        z = z * weights
    return np.sum(z) if not axis else np.sum(z, axis=axis)

def manhattan(x, y, weights=None, axis=None):
    z = np.abs(x - y)
    if weights:
        z = z * weights
    return np.sum(z) if not axis else np.sum(z, axis=axis)

def minkowski(x, y, p=2, weights=None, axis=None):
    z = np.power(np.abs(x - y), p)
    if weights:
        z = z * weights
    return np.sum(z) if not axis else np.sum(z, axis=axis)

def cosine(x, y, axis=None):
    if axis:
        z = np.sum(x*y, axis=axis) / np.sqrt(
            np.sum(np.power(x, 2), axis=axis) *
            np.sum(np.power(y, 2), axis=axis)
        )
    else:
        z = np.sum(x * y) / np.sqrt(
            np.sum(np.power(x, 2)) *
            np.sum(np.power(y, 2))
        )
    return z