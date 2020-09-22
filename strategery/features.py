from strategery.exceptions import TaskError


class StrategeryFeature(object):
    def __init__(self, unique_key=None):
        self.unique_key = unique_key
        if unique_key is None:
            self.unique_key = type(self)

    def __hash__(self):
        return hash(self.unique_key)

    def __eq__(self, other):
        return self.unique_key == other

    def _assert_has_unique_key(self):
        if not hasattr(self, 'unique_key'):
            raise TaskError('Subclasses of StrategeryFeature must call super().__init__(unique_key=[optional]).\n' + \
                            'Task {t}, found at "{f}:{l}".'.format(
                                t=self.name,
                                f=self.code_file_name,
                                l=self.code_first_line_number
                            ))

    @property
    def dependencies(self):
        return self.__call__.dependencies