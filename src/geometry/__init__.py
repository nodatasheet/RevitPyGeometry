"""
Geometry primitives wrapped around Revit geometry objects.
"""

import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit import DB

from point import Point2D, Point3D

__all__ = [
    'Point2D', 'Point3D'
]
