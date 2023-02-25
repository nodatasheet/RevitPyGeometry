"""Vectors and Vectors"""

from abc import ABCMeta

from entity import GeometryEntity
from utils import are_numbers_close
from abstract_revit import (
    AbstractRevitCoordinates, AbstractRevitUV, AbstractRevitXYZ
)


class Vector(GeometryEntity):
    """Base class for vectors."""

    __metaclass__ = ABCMeta

    _coordinates = tuple()
    _rvt_obj = None  # type: AbstractRevitCoordinates
    revit_type = None

    def __new__(cls, *args, **kwargs):
        if cls is Vector:
            raise TypeError('Creating instances of Vector is not allowed.')
        return super(Vector, cls).__new__(cls)

    def __str__(self):
        return self.__class__.__name__ + str(self._coordinates)

    def __abs__(self):
        """Returns the distance between this vector and the origin."""
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
        # type: (float) -> Vector
        """Multiply vector's coordinates by a factor."""
        return self._wrap(
            self._rvt_obj.Multiply(factor)
        )

    def __rmul__(self, factor):
        """Multiply a factor by vector's coordinates."""
        return self.__mul__(factor)

    def __neg__(self):
        """Negate the vector."""
        return self._wrap(
            self._rvt_obj.Negate()
        )

    def __add__(self, other):
        # type: (Vector) -> Vector
        """Add other to self by incrementing self's coordinates by
        those of other.
        """
        return self._wrap(
            self._rvt_obj.Add(other._rvt_obj)
        )

    def __sub__(self, other):
        # type: (Vector) -> Vector
        """Subtract two vectors."""
        return self._wrap(
            self._rvt_obj.Subtract(other._rvt_obj)
        )

    def __lt__(self, other):
        # type: (Vector) -> bool
        raise NotImplementedError()

    def __eq__(self, other):
        # type: (Vector) -> bool
        """Check vectors equality using `is_almost_equal_to()` method
        with the default tolerance.

        For more precise equality, use `is_are_numbers_close_to()`
        with specified tolerance.
        """
        return self.is_almost_equal_to(other)

    def __ne__(self, other):
        # type: (Vector) -> bool
        return not self.__eq__(other)

    def __gt__(self, other):
        # type: (Vector) -> bool
        return not self.__lt__(other) and self.__ne__(other)

    def __le__(self, other):
        # type: (Vector) -> bool
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        # type: (Vector) -> bool
        return not self.__lt__(other)

    def to_vector(self):
        raise NotImplementedError()

    def to_point(self):
        raise NotImplementedError()

    def is_almost_equal_to(self, other, tolerance=None):
        # type: (Vector, float) -> bool
        """Checks whether this vector and other vector are the same
        withing a specified tolerance.

        If no tolerance specified, used Revit default tolerance
        of vectors comparison.
        """
        if tolerance is not None:
            return self._rvt_obj.IsAlmostEqualTo(other._rvt_obj, tolerance)
        return self._rvt_obj.IsAlmostEqualTo(other._rvt_obj)

    def distance_to(self, other):
        # type: (Vector) -> float
        return self._rvt_obj.DistanceTo(other._rvt_obj)

    def dot_product(self, other):
        # type: (Vector) -> float
        return self._rvt_obj.DotProduct(other._rvt_obj)

    def cross_product(self, other):
        # type: (Vector) -> Vector
        return self._wrap(
            self._rvt_obj.CrossProduct(other._rvt_obj)
        )

    def multiply(self, other):
        # type: (float) -> Vector
        return self._wrap(
            self._rvt_obj.Multiply(other._rvt_obj)
        )

    def _wrap(self, rvt_obj):
        # type: (AbstractRevitCoordinates) -> Vector
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
        """A vector of all zero coordinates."""
        return self._wrap(self._rvt_obj.Zero)

    @property
    def is_zero(self):
        # type: () -> bool
        """True if every coordinate is zero, False otherwise"""
        return self._rvt_obj.IsZeroLength()


class Vector2D(Vector):
    """Vector in a 2-dimensional space."""

    def __init__(self, revit_uv):
        # type: (AbstractRevitUV) -> None
        self._rvt_obj = revit_uv
        self._coordinates = (self._rvt_obj.U,
                             self._rvt_obj.V)

    def __lt__(self, other):
        # type: (Vector) -> bool
        """Is vector smaller than other.

        Used first method from here:
        https://math.stackexchange.com/a/54657

        p1.x < p2.x

        or p1.x = p2.x and p1.y < p2.y

        Equality is approximate.
        """
        self._validate_type(other, type(self))

        if self.x < other.x:
            return True

        if are_numbers_close(self.x, other.x) and self.y < other.y:
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


class Vector3D(Vector):
    """Vector in a 3-dimensional space."""

    def __init__(self, revit_xyz):
        # type: (AbstractRevitXYZ) -> None
        self._rvt_obj = revit_xyz
        self._coordinates = (self._rvt_obj.X,
                             self._rvt_obj.Y,
                             self._rvt_obj.Z)

    def __lt__(self, other):
        # type: (Vector) -> bool
        """Is vector smaller than other.

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

        if are_numbers_close(self.x, other.x):
            if self.y < other.y:
                return True

            if self.z < other.z and are_numbers_close(self.y, other.y):
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


class Point2D(Vector2D):
    pass


class Point3D(Vector3D):
    pass
