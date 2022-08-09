from xmlrpc.client import Boolean
from bezier import Curve

class FakePolygon:
    """The curves of a curved polygon"""
    def __init__(self, curves: list[Curve]):
        self.curves = curves

    def intersects_curve(self, curve: Curve) -> Boolean:
        for own_curve in self.curves:
            if own_curve.intersect(curve).size > 0:
                return True
        return False
    
class FakePolygonCollection:
    """A collection of FakePolygon's that should light up together"""
    def __init__(self, polygons: list[FakePolygon]):
        self.polygons = polygons

    def any_intersect(self, curve:Curve) -> Boolean:
        for polygon in self.polygons:
            if polygon.intersects_curve(curve):
                return True

        return False