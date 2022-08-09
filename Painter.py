# Tools to paint a bezier curve using its intersection with a collection of curved polygons.

# https://github.com/dhermes/bezier/issues/237
from bezier import Curve, CurvedPolygon
import Common
from matplotlib.artist import Artist
from matplotlib.pyplot import plot
import Curves
import Grids

def find_intersecting_polygons(polygon_collections: list[Common.FakePolygonCollection], lines: list[Curve]) -> list[Common.FakePolygonCollection]:
    # Returns the sub-list of polygons (passed in as lists of Curves) that intersect the curve `line`
    ret_list = []
    for polygon_collection in polygon_collections:
        for line in lines:
            if polygon_collection.any_intersect(line):
                ret_list.append(polygon_collection)
                break

    return ret_list

def paint_polygons(plot_axis: Artist, polygon_collections: list[Common.FakePolygonCollection], points_per_edge=100, color=(1,1,1)):
    for polygon_collection in polygon_collections:
        for polygon in polygon_collection.polygons:
            curved_polygon = CurvedPolygon(*polygon.curves)

            curved_polygon.plot(points_per_edge, color, plot_axis)