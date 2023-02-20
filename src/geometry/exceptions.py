
class GeometryException(Exception):
    pass


class IOException(GeometryException):
    pass


class ValidationException(GeometryException):
    pass


class TypeValidationException(GeometryException):
    pass
