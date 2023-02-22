"""Geometrical Points."""
from abc import ABCMeta, abstractmethod, abstractproperty
from entity import GeometryEntity


class AbstractRevitCoordinates(object):

    @abstractmethod
    def Add(self, other):
        # type: (AbstractRevitCoordinates) -> AbstractRevitCoordinates
        pass

    @abstractmethod
    def AngleTo(self, other):
        # type: (AbstractRevitCoordinates) -> AbstractRevitCoordinates
        pass

    @abstractmethod
    def CrossProduct(self, other):
        # type: (AbstractRevitCoordinates) -> float
        pass

    @abstractmethod
    def Divide(self, value):
        # type: (float) -> AbstractRevitCoordinates
        pass

    @abstractmethod
    def DistanceTo(self, other):
        # type: (AbstractRevitCoordinates) -> float
        pass

    @abstractmethod
    def DotProduct(self, other):
        # type: (AbstractRevitCoordinates) -> float
        pass

    @abstractmethod
    def IsAlmostEqualTo(self, other):
        # type: (AbstractRevitCoordinates) -> bool
        pass

    @abstractmethod
    def IsUnitLength(self):
        # type: () -> bool
        pass

    @abstractmethod
    def IsZeroLength(self):
        # type: () -> bool
        pass

    @abstractmethod
    def Multiply(self, value):
        # type: (float) -> AbstractRevitCoordinates
        pass

    @abstractmethod
    def Negate(self):
        # type: () -> AbstractRevitCoordinates
        pass

    @abstractmethod
    def Normalize(self):
        # type: () -> AbstractRevitCoordinates
        pass

    @abstractmethod
    def Subtract(self, other):
        # type: (AbstractRevitCoordinates) -> AbstractRevitCoordinates
        pass

    @abstractproperty
    def Zero(self):
        # type: () -> AbstractRevitCoordinates
        pass


class AbstractRevitUV(AbstractRevitCoordinates):

    @abstractproperty
    def U(self):
        # type: () -> float
        pass

    @abstractproperty
    def V(self):
        # type: () -> float
        pass


class AbstractRevitXYZ(AbstractRevitCoordinates):

    @abstractproperty
    def X(self):
        # type: () -> float
        pass

    @abstractproperty
    def Y(self):
        # type: () -> float
        pass

    @abstractproperty
    def Z(self):
        # type: () -> float
        pass


class Point(GeometryEntity):
    """Base class for points."""

    __metaclass__ = ABCMeta

    _coordinates = tuple()
    _rvt_obj = None  # type: AbstractRevitCoordinates
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
        return self.distance_to(self.origin)

    def __contains__(self, item):
        return item in self._coordinates

    def __getitem__(self, key):
        return self._coordinates[key]

    def __iter__(self):
        return self._coordinates.__iter__()

    def __len__(self):
        return len(self._coordinates)

    def add(self, other):
        # type: (Point) -> Point
        """Add other to self by incrementing self's coordinates by
        those of other.
        """
        return self._rvt_obj.Add(other._rvt_obj)

    def distance_to(self, other):
        # type: (Point) -> float
        return self._rvt_obj.DistanceTo(other._rvt_obj)

    def multiply(self, other):
        # type: (float) -> Point
        return self._rvt_obj.Multiply(other._rvt_obj)

    @property
    def coordinates(self):
        # type: () -> tuple[float]
        return self._coordinates

    @property
    def revit_object(self):
        """Gets the revit object which stands behind this wrap."""
        return self._rvt_obj

    @property
    def origin(self):
        """A point of all zero coordinates."""
        return self.__class__(self._rvt_obj.Zero)


class Point2D(Point):
    """Point in a 2-dimensional space."""

    def __init__(self, revit_uv):
        # type: (AbstractRevitUV) -> None
        self._rvt_obj = revit_uv
        self._coordinates = (self._rvt_obj.U,
                             self._rvt_obj.V)


class Point3D(Point):
    """Point in a 3-dimensional space."""

    def __init__(self, revit_xyz):
        # type: (AbstractRevitXYZ) -> None
        self._rvt_obj = revit_xyz
        self._coordinates = (self._rvt_obj.X,
                             self._rvt_obj.Y,
                             self._rvt_obj.Z)
