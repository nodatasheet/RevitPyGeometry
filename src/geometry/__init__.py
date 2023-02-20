"""
Geometry primitives wrapped around Revit geometry objects.

"""

from geometry.exceptions import TypeValidationException


class GeometryEntity(object):
    """The base class for all geometrical entities.

    This class does not represent any particular geometric entity, it only
    provides the implementation of some methods common to all subclasses.

    """

    def _validate_type(self, obj, expected_type):
        # type: (object, type) -> None
        if not isinstance(obj, expected_type):
            raise TypeValidationException(
                'Expected <{}>, got <{}>'.format(expected_type.__name__,
                                                 type(obj).__name__))
