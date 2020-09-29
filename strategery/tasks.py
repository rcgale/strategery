import inspect

from strategery.exceptions import TaskError
from strategery.features import StrategeryFeature


class Task(object):
    def __init__(self, task):
        self._task = task
        self.dependencies = tuple()
        self.signature = tuple()
        self.parameters = {}
        if hasattr(self._task, '_dependencies'):
            self.dependencies = self._task._dependencies
            self.signature = inspect.signature(self._task)
            self.parameters = self.signature.parameters
        elif isinstance(task, StrategeryFeature):
            self._assert_has_unique_key()
        elif hasattr(self._task, '__call__') and hasattr(self._task.__call__, '_dependencies'):
            raise TaskError('Instance tasks should inherit from StrategeryFeature class.\n' + \
                            'Task {t}, found at "{f}:{l}".'.format(
                                t=self.name,
                                f=self.code_file_name,
                                l=self.code_first_line_number
                            ))

    @property
    def name(self):
        if isinstance(self._task, str):
            return "'{}'".format(self._task)
        module = ""
        if hasattr(self._task, '__module__'):
            module = '{}.'.format(self._task.__module__)
        if hasattr(self._task, '__class__') and hasattr(self._task.__class__, '__qualname__'):
            return '{}{}'.format(module, self._task.__class__.__qualname__)
        if hasattr(self._task, '__name__'):
            return '{}{}'.format(module, self._task.__name__)
        return '{}{}'.format(module, type(self._task).__name__)


    @property
    def code_first_line_number(self):
        try:
            if not self.callable():
                return None
            if hasattr(self._task, '__code__'):
                return self._task.__code__.co_firstlineno
            return inspect.findsource(type(self._task))[1]
        except:
            return '(unknown line number)'

    @property
    def code_file_name(self):
        try:
            return inspect.getmodule(self._task).__file__
        except:
            return '(unknown file)'

    def _assert_has_unique_key(self):
        if not hasattr(self._task, '_unique_key'):
            raise TaskError('Subclasses of StrategeryFeature must call super().__init__(unique_key=[optional]).\n' + \
                            'Task {t}, found at "{f}:{l}".'.format(
                                t=self.name,
                                f=self.code_file_name,
                                l=self.code_first_line_number
                            ))

    def callable(self):
        return callable(self._task)

    def __call__(self, *args, **kwargs):
        return self._task.__call__(*args, **kwargs)

    def __hash__(self):
        return hash(self._task)

    def __eq__(self, other):
        return self._task == other

    def __str__(self):
        return 'Strategery Task: {}'.format(self._task)
