"""Geometrical Points."""
from abc import ABCMeta, abstractmethod
from entity import GeometryEntity


class AbstractRevitObject(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def DistanceTo(self, other):
        # type: (AbstractRevitObject) -> AbstractRevitObject
        pass


class AbstractRevitUV(AbstractRevitObject):
    pass


class AbstractRevitXYZ(AbstractRevitObject):
    pass


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

    __metaclass__ = ABCMeta

    _coordinates = tuple()
    _rvt_obj = None  # type: AbstractRevitObject
    revit_type = None

    def __new__(cls, *args, **kwargs):
        if cls is Point:
            raise TypeError('Cannot create instances of Point '
                            'because it has no public constructors.')
        return super(Point, cls).__new__(cls)

    def __str__(self):
        return self.__class__.__name__ + str(self._coordinates)

    def __abs__(self):
        """Returns the distance between this point and the origin."""
        # origin = Point([0]*len(self))
        # return Point.distance(origin, self)
        pass

    def distance_to(self, other):
        # type: (Point) -> float
        return self._rvt_obj.DistanceTo(other._rvt_obj)

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

    def __init__(self, uv_revit_point):
        # type: (AbstractRevitUV) -> None
        self._rvt_obj = uv_revit_point
        self._coordinates = (self._rvt_obj.U,
                             self._rvt_obj.V)


class Point3D(Point):
    """Point in a 3-dimensional space."""

    def __init__(self, xyz_revit_point):
        # type: (AbstractRevitXYZ) -> None
        self._rvt_obj = xyz_revit_point
        self._coordinates = (self._rvt_obj.X,
                             self._rvt_obj.Y,
                             self._rvt_obj.Z)
