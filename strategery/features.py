from strategery.exceptions import TaskError


class StrategeryFeature(object):
    def __init__(self, unique_key=None):
        self._unique_key = unique_key
        if unique_key is None:
            self._unique_key = type(self)
        self._dependencies = tuple()
        if hasattr(self, '__call__') and hasattr(self.__call__, '_dependencies'):
            self._dependencies = self.__call__._dependencies

    def __hash__(self):
        return hash(self._unique_key)

    def __eq__(self, other):
        return self._unique_key == other
