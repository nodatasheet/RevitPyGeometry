"""Geometrical Points."""

from . import DB
from .entity import GeometryEntity


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, class_=None):
        if class_ is None:
            class_ = type(obj)
        return self.fget.__get__(obj, class_)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


class Point(GeometryEntity):
    """Base class for points."""

    _ambient_dimension = 0
    _coordinates = tuple()
    _rvt_obj = None

    def __init__(self, *args):
        if not args:
            args = self._get_zero_coords()
            return self.__init__(*args)
        self._validate_attr_qty(self._ambient_dimension, len(args))
        self._coordinates = (args)

    def __str__(self):
        return self.__class__.__name__ + str(self._coordinates)

    def __abs__(self):
        """Returns the distance between this point and the origin."""
        # origin = Point([0]*len(self))
        # return Point.distance(origin, self)
        pass

    def distance_to(self, other_point):
        # type: (Point) -> float
        # return itemgetter (self._rvt_obj)
        pass

    @classmethod
    def _get_origin_point(cls):
        zeros = cls._get_zero_coords()
        return cls(*zeros)

    @classmethod
    def _get_zero_coords(cls):
        return tuple(0 for _ in range(cls._ambient_dimension))

    @property
    def coordinates(self):
        # type: () -> tuple[float]
        return self.coordinates

    @property
    def revit_object(self):
        """Gets the revit object which stands behind this wrap."""
        return self._rvt_obj

    @classproperty
    def origin(cls):
        """A point of all zero coordinates."""
        return cls._get_origin_point()


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
