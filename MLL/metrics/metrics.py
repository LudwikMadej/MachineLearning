import numpy as np

def fetch_metric(metric_name, *args):
    if metric_name in ['l2', 'euclidean']:
        return euclidean

    if metric_name in ['l1', 'manhattan']:
        return manhattan

    if metric_name == 'minkowski':
        return generate_minskowski(*args)

    if metric_name == 'cosine':
        return cosine

    return None

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

def generate_minskowski(p=2, weights=None, axis=None):
    def minkowski_(x, y):
        z = np.power(np.abs(x - y), p)
        if weights:
            z = z * weights
        return np.sum(z) if not axis else np.sum(z, axis=axis)
    return minkowski_

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