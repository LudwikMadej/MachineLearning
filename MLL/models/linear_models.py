import numpy as np
from model import Model

class LinearRegressor(Model):
    def __init__(self):
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        if X.shape[0] != y.shape[0]:
            raise Exception(
                """
                Number of rows in X doesn't match shape of y
                """
                            )

        if len(X.shape) != 2:
            raise Exception(
                """
                    X must be a 2-dimensional array
                """
            )

        X = np.concat([X, np.ones(X.shape[0]).reshape([-1, 1])], axis=1)
        solution = np.linalg.pinv(X.T @ X) @ X.T @ y.reshape([-1, 1])
        self.coef_ = solution[:-1].reshape([-1, 1])
        self.intercept_ = solution[-1]

    def predict(self, X):
        return  X @ self.coef_ + self.intercept_