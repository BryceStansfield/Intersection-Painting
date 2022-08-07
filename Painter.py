# Tools to paint a bezier curve using its intersection with a collection of curved polygons.

# https://github.com/dhermes/bezier/issues/237
from bezier import Curve, CurvedPolygon
from matplotlib.artist import Artist
from matplotlib.pyplot import plot
import Curves
import Grids

def find_intersecting_polygons(polygons: list[list[Curve]], lines: list[Curve]) -> list[list[Curve]]:
    # Returns the sub-list of polygons (passed in as lists of Curves) that intersect the curve `line`
    ret_list = []
    for polygon in polygons:
        polygon_done = False
        for segment in polygon:
            for line in lines:
                if segment.intersect(line).size > 0:
                    ret_list.append(polygon)
                    polygon_done = True
                    break
            if polygon_done:
                break
    
    return ret_list

def paint_polygons(plot_axis: Artist, polygons: list[list[Curve]], points_per_edge=100, color=(1,1,1)):
    for polygon in polygons:
        curved_polygon = CurvedPolygon(*polygon)

        curved_polygon.plot(points_per_edge, color, plot_axis)

#if __name__ == "__main__":
#    test_grid = Grids.pixel_grid(10, 10, (100, 100,))
#    bezier_circle = Curves.approximate_circle((50, 50), 50)
#    print(len(test_grid), len(find_intersecting_polygons(test_grid, bezier_circle)))
