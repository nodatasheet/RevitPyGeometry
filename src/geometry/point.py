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
        # type: (AbstractRevitCoordinates) -> AbstractRevitCoordinates
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

    def __mul__(self, factor):
        # type: (float) -> Point
        """Multiply point's coordinates by a factor."""
        return self._wrap(
            self._rvt_obj.Multiply(factor)
        )

    def __rmul__(self, factor):
        """Multiply a factor by point's coordinates."""
        return self.__mul__(factor)

    def __neg__(self):
        """Negate the point."""
        return self._wrap(
            self._rvt_obj.Negate()
        )

    def __add__(self, other):
        # type: (Point) -> Point
        """Add other to self by incrementing self's coordinates by
        those of other.
        """
        return self._wrap(
            self._rvt_obj.Add(other._rvt_obj)
        )

    def __sub__(self, other):
        # type: (Point) -> Point
        """Subtract two points."""
        return self._wrap(
            self._rvt_obj.Subtract(other._rvt_obj)
        )

    def __lt__(self, other):
        # type: (Point) -> bool
        raise NotImplementedError(
            'This method should be overwritten in child classes')

    def __eq__(self, other):
        # type: (Point) -> bool
        """Check points equality using `is_almost_equal_to()` method
        with the default tolerance.

        For more precise equality, use `is_almost_equal_to()`
        with specified tolerance.
        """
        return self.is_almost_equal_to(other)

    def __ne__(self, other):
        # type: (Point) -> bool
        return not self.__eq__(other)

    def __gt__(self, other):
        # type: (Point) -> bool
        return not self.__lt__(other) and self.__ne__(other)

    def __le__(self, other):
        # type: (Point) -> bool
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        # type: (Point) -> bool
        return not self.__lt__(other)

    def is_almost_equal_to(self, other, tolerance=None):
        # type: (Point, float) -> bool
        """Checks whether this point and other point are the same
        withing a specified tolerance.

        If no tolerance specified, used Revit default tolerance
        of points comparison.
        """
        if tolerance is not None:
            return self._rvt_obj.IsAlmostEqualTo(other._rvt_obj, tolerance)
        return self._rvt_obj.IsAlmostEqualTo(other._rvt_obj)

    def distance_to(self, other):
        # type: (Point) -> float
        return self._rvt_obj.DistanceTo(other._rvt_obj)

    def dot_product(self, other):
        # type: (Point) -> float
        return self._rvt_obj.DotProduct(other._rvt_obj)

    def cross_product(self, other):
        # type: (Point) -> Point
        return self._wrap(
            self._rvt_obj.CrossProduct(other._rvt_obj)
        )

    def multiply(self, other):
        # type: (float) -> Point
        return self._wrap(
            self._rvt_obj.Multiply(other._rvt_obj)
        )

    def _wrap(self, rvt_obj):
        # type: (AbstractRevitCoordinates) -> Point
        return self.__class__(rvt_obj)

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
        return self._wrap(self._rvt_obj.Zero)

    @property
    def is_zero(self):
        # type: () -> bool
        """True if every coordinate is zero, False otherwise"""
        return self._rvt_obj.IsZeroLength()


class Point2D(Point):
    """Point in a 2-dimensional space."""

    def __init__(self, revit_uv):
        # type: (AbstractRevitUV) -> None
        self._rvt_obj = revit_uv
        self._coordinates = (self._rvt_obj.U,
                             self._rvt_obj.V)

    def __lt__(self, other):
        # type: (Point) -> bool
        """Is point smaller than other.

        Used first method from here:
        https://math.stackexchange.com/a/54657
        """
        self._validate_type(other, type(self))

        if self.x < other.x:
            return True

        if almost_equal(self.x, other.x) and self.y < other.y:
            return True

        return False

    @property
    def x(self):
        # type: () -> float
        return self._rvt_obj.U

    @property
    def y(self):
        # type: () -> float
        return self._rvt_obj.V


class Point3D(Point):
    """Point in a 3-dimensional space."""

    def __init__(self, revit_xyz):
        # type: (AbstractRevitXYZ) -> None
        self._rvt_obj = revit_xyz
        self._coordinates = (self._rvt_obj.X,
                             self._rvt_obj.Y,
                             self._rvt_obj.Z)

    def __lt__(self, other):
        # type: (Point) -> bool
        """Is point smaller than other.

        Used first method from here:
        https://math.stackexchange.com/a/54657

        p1.x < p2.x

        or p1.x = p2.x and p1.y = p2.y

        or p1.x = p2.x and p1.y = p2.y and p1.z < p2.z

        Equality is approximate.
        """
        self._validate_type(other, type(self))

        if self.x < other.x:
            return True

        if almost_equal(self.x, other.x):
            if self.y < other.y:
                return True

            if self.z < other.z and almost_equal(self.y, other.y):
                return True

        return False

    @property
    def x(self):
        # type: () -> float
        return self._rvt_obj.X

    @property
    def y(self):
        # type: () -> float
        return self._rvt_obj.Y

    @property
    def z(self):
        # type: () -> float
        return self._rvt_obj.Z


def almost_equal(a, b, rel_tol=1e-09, abs_tol=0.0):
    """A function for testing approximate equality of two numbers.
    Same as math.isclose in Python v3.5 (and newer)
    https://www.python.org/dev/peps/pep-0485
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
