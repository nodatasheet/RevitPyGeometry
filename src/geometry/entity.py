"""The definition of the base geometrical entity with attributes common to
all derived geometrical entities.
"""
from abc import ABCMeta
from exceptions import TypeValidationException


class GeometryEntity(object):
    """The base class for all geometrical entities."""

    __metaclass__ = ABCMeta

    def __new__(cls, *args, **kwargs):
        if cls is GeometryEntity:
            raise TypeError('Cannot create instances of GeometryEntity '
                            'because it has no public constructors.')
        return super(GeometryEntity, cls).__new__(cls)

    def _validate_type(self, obj, expected_type):
        # type: (object, type) -> None
        if not isinstance(obj, expected_type):
            raise TypeValidationException(type(obj), expected_type)
