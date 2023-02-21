
class GeometryException(Exception):
    pass


class IOException(GeometryException):
    pass


class ValidationException(GeometryException):
    pass


class TypeValidationException(ValidationException):

    _message = None

    def __init__(self, expected_type, current_type):
        # type: (type, type) -> None
        self._expected_type = expected_type
        self._current_type = current_type

        self._expected_type_name = expected_type.__name__
        self._current_type_name = current_type.__name__

    def __str__(self):
        # type: () -> str
        if self._message is None:
            self.message = 'Expected <{}>, got <{}>'.format(
                self._expected_type_name, self._current_type_name)

        return self._message

    @property
    def message(self):
        # type: () -> str
        return self._message

    @message.setter
    def message(self, value):
        # type: (str) -> None
        self._message = value
