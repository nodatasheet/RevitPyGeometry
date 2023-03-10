"""Utilities for geometry objects."""


def are_numbers_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    """A function for testing approximate equality of two numbers.
    Same as math.isclose in Python v3.5 (and newer)
    https://www.python.org/dev/peps/pep-0485
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
