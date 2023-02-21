
class GeometryException(Exception):
    pass


class IOException(GeometryException):
    pass


class ValidationException(GeometryException):
    pass


class TypeError(GeometryException):
    pass


class TypeValidationException(GeometryException):
    pass


def raise_wrong_type(obj, expected_type):
    # type: (object, type) -> None
    raise TypeValidationException(
        'Expected <{}>, got <{}>'.format(expected_type.__name__,
                                         type(obj).__name__)
    )


def raise_wrong_attr_qty(qty_expected, qty_got):
    # type: (int, int) -> None
    raise TypeError(
        'expected {} arguments, got {}'.format(qty_expected, qty_got)
    )
