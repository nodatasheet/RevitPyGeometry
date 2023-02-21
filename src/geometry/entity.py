"""The definition of the base geometrical entity with attributes common to
all derived geometrical entities.
"""

from exceptions import raise_wrong_attr_qty, raise_wrong_type


class GeometryEntity(object):
    """The base class for all geometrical entities."""

    def _validate_type(self, obj, expected_type):
        # type: (object, type) -> None
        if not isinstance(obj, expected_type):
            raise_wrong_type(obj, expected_type)

    def _validate_attr_qty(self, qty_expected, qty_got):
        # type: (int, int) -> None
        if qty_expected != qty_got:
            raise_wrong_attr_qty(qty_expected, qty_got)
