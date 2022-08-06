# Tools to paint a bezier curve using its intersection with a collection of curved polygons.

# https://github.com/dhermes/bezier/issues/237
from bezier import Curve, CurvedPolygon
from matplotlib.artist import Artist
from matplotlib.pyplot import plot

def find_intersecting_polygons(polygons: list[list[Curve]], line: Curve) -> list[CurvedPolygon]:
    # Returns the sub-list of polygons (passed in as lists of Curves) that intersect the curve `line`
    ret_list = []
    for polygon in polygons:
        for segment in polygon:
            if len(segment.intersect(line)) > 0:
                ret_list.append(polygon)
                break

    return ret_list

def paint_polygons(plot_axis: Artist, polygons: list[list[Curve]], points_per_edge=100, color=(1,1,1)):
    for polygon in polygons:
        curved_polygon = CurvedPolygon(*polygon)

        curved_polygon.plot(points_per_edge, color, plot_axis)
