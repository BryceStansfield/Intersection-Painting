# Tools to paint a bezier curve using its intersection with a collection of curved polygons.

# https://github.com/dhermes/bezier/issues/237
from tracemalloc import start
from bezier import Curve, CurvedPolygon
import Common
from matplotlib.artist import Artist
from matplotlib.pyplot import plot
import Curves
import Grids
from typing import Tuple

def find_intersecting_polygons(grid_size: tuple[float, float], polygon_collections: list[Common.FakePolygonCollection], already_collided, collider: Common.Collider) -> list[int]:
    # Returns the (intersecting polygonCollections, non-intersecting polygonCollections) 
    intersecting_list = []

    has_already_collided = False
    for i, polygon_collection in enumerate(polygon_collections):
        if not has_already_collided or (i not in already_collided):
            for line in collider.curves:
                if polygon_collection.any_intersect(line):
                    if i not in already_collided:
                        intersecting_list.append(i)
                    has_already_collided = True
                    break

    if len(intersecting_list) != 0 or has_already_collided:
        return intersecting_list
    
    # We're entirely within some polygon, let's figure out which one it is
    # WARNING: Super inefficient, but I'm making a gpu version later, so I don't care for now
    # WARNING 2: Assumes that no polygon surrounds another by more than 270 degrees, will crash if so
    def direction_intersect_list(dir):
        # Poke a line to the left/right of the first point in our curves, to see what we're inside of
        start_point = collider.curves[0].nodes[[0,1],[0]]
        currently_intersecting = []

        if dir == 'up':
            current_intersection_bisect = [0, grid_size[1]-start_point[1] + 0.1]
        elif dir =='down':
            current_intersection_bisect = [0, start_point[1] + 0.1]
        elif dir == 'left':
            current_intersection_bisect = [0, start_point[0] + 0.1]
        elif dir == 'right':
            current_intersection_bisect = [0, grid_size[0]-start_point[0] + 0.1]

        while len(currently_intersecting) != 2 and len(currently_intersecting) != 1:
            currently_intersecting = []
            middle_bisect_point = (current_intersection_bisect[0] + current_intersection_bisect[1])/2

            x_2 = start_point[0]
            y_2 = start_point[1]

            if dir == 'left':
                x_2 -= middle_bisect_point
            elif dir == 'right':
                x_2 += middle_bisect_point
            elif dir == 'up':
                y_2 += middle_bisect_point
            elif dir == 'down':
                y_2 -= middle_bisect_point

            new_curve = Curve([[start_point[0], x_2],[start_point[1], y_2]], 1)
            
            for i, polygon_collection in enumerate(polygon_collections):
                if polygon_collection.any_intersect(new_curve):
                    currently_intersecting.append(i)
                
            if len(currently_intersecting) > 2:
                current_intersection_bisect[1] = middle_bisect_point

            elif len(currently_intersecting) == 0:
                current_intersection_bisect[0] = middle_bisect_point
        return currently_intersecting
    
    intersecting_lists = [direction_intersect_list(x) for x in ['up', 'down', 'left', 'right']]
    i = intersecting_lists[0][0]
    if i in intersecting_lists[0] and i in intersecting_lists[1] and i in intersecting_lists[2] and i in intersecting_lists[3]:
        return [i]
    return [intersecting_lists[0][1]]

def paint_polygons(plot_axis: Artist, polygon_collections: list[Common.FakePolygonCollection], color, points_per_edge=100):
    for polygon_collection in polygon_collections:
        for polygon in polygon_collection.polygons:
            curved_polygon = CurvedPolygon(*polygon.curves)

            curved_polygon.plot(points_per_edge, color, plot_axis)

def paint_intersecting_polygons(plot_axis: Artist, grid: list[Common.FakePolygonCollection], grid_size: tuple[float, float], colliders: list[Common.Collider], points_per_edge=100):
    """Paints where colliders intersect with our grid, on axis plot_axis and with earlier colliders taking precedence (e.g. colliders[n] is painted over colliders[n+1])"""
    already_collided = set()

    for collider in colliders:
        new_collisions = find_intersecting_polygons(grid_size, grid, already_collided, collider)
        for x in new_collisions:
            already_collided.add(x)

        paint_polygons(plot_axis, [grid[i] for i in new_collisions], collider.colour, points_per_edge=points_per_edge)