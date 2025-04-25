from abc import ABC, abstractmethod

@ABC
class Model:
    def __init__(self, random_state=None):
        self.random_state = random_state


    @abstractmethod
    def fit(self, X, y, warm_start=False):
        pass

    @abstractmethod
    def predict(self):
        pass
