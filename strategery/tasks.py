import inspect

from strategery.exceptions import TaskError


class Task(object):
    def __init__(self, task):
        self._task = task
        self.dependencies = tuple()
        self.signature = tuple()
        if hasattr(self._task, 'dependencies'):
            self.dependencies = self._task.dependencies
            self.signature = inspect.signature(self._task)
        elif hasattr(self._task, '__call__') and hasattr(self._task.__call__, 'dependencies'):
            raise TaskError('Instance tasks should inherit from StrategeryFeature class.\n' + \
                            'Task {t}, found at "{f}:{l}".'.format(
                                t=self.name,
                                f=self.code_file_name,
                                l=self.code_first_line_number
                            ))

    @property
    def name(self):
        if hasattr(self._task, '__name__'):
            return self._task.__name__
        return type(self._task).__name__


    @property
    def code_first_line_number(self):
        if not self.callable():
            return None
        if hasattr(self._task, '__code__'):
            return self._task.__code__.co_firstlineno
        return inspect.findsource(type(self._task))[1]

    @property
    def code_file_name(self):
        try:
            return inspect.getmodule(self._task).__file__
        except:
            return '(unknown file)'

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
