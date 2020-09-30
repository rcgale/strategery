from abc import abstractmethod

from strategery.exceptions import TaskError


class StrategeryFeature(object):
    @classmethod
    def key(cls):
        return cls

    @staticmethod
    @abstractmethod
    def compute(*args, **kwargs):
        raise NotImplementedError('StrategeryFeature must implement @staticmethod `compute`!')
