"""Geometrical Points."""

from . import DB
from .entity import GeometryEntity


class Point(GeometryEntity):
    """Base class for points."""

    _ambient_dimension = 0
    _coordinates = tuple()
    _rvt_obj = None

    def __init__(self, *args):
        self._validate_attr_qty(self._ambient_dimension, len(args))
        self._coordinates = (args)

    def __str__(self):
        return self.__class__.__name__ + str(self._coordinates)

    @property
    def coordinates(self):
        # type: () -> tuple[float]
        return self.coordinates

    @property
    def revit_object(self):
        """Gets the revit object which stands behind this wrap."""
        return self._rvt_obj


class Point2D(Point):
    """Point in a 2-dimensional space."""

    _ambient_dimension = 2

    def __init__(self, *args):
        super(Point2D, self).__init__(*args)
        self._rvt_obj = DB.UV(*args)


class Point3D(Point):
    """Point in a 3-dimensional space."""
    _ambient_dimension = 3

    def __init__(self, *args):
        super(Point3D, self).__init__(*args)
        self._rvt_obj = DB.XYZ(*args)
