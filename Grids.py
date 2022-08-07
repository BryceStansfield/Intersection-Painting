# Grids.py contains a set of functions which generate grids of curved polgons covering the set [0,1]^2
from bezier import Curve
import numpy as np

def pixel_grid(num_x, num_y, grid_size) -> list[list[Curve]]:
    polygons = []
    for x in range(num_x):
        for y in range(num_y):
            # Constructing a square
            start_x = (x*grid_size[0])/num_x
            end_x = ((x+1)*grid_size[0])/num_x
            start_y = (y*grid_size[1])/num_y
            end_y = ((y+1)*grid_size[1])/num_y

            polygons.append([
                Curve(np.asfortranarray([[start_x, start_x], [start_y, end_y]]), degree=1),
                Curve(np.asfortranarray([[start_x, end_x], [end_y, end_y]]), degree=1),
                Curve(np.asfortranarray([[end_x, end_x], [end_y, start_y]]), degree=1),
                Curve(np.asfortranarray([[end_x, start_x], [start_y, start_y]]), degree=1)
                ]
            )

    return polygons

def sierpinski_triangle(num_iterations, square_size) -> list[list[Curve]]:
    triangle_segments = []
    
    # First let's add the "gaps"
    # The left and right gaps are special and should be dealt with seperately
    triangle_segments.append([  # Left
        Curve(np.asfortranarray([[0.0, square_size/2], [square_size, square_size]]), degree=1),
        Curve(np.asfortranarray([[square_size/2, 0.0], [square_size, 0.0]]), degree=1),
        Curve(np.asfortranarray([[0.0, 0.0], [0.0, square_size]]), degree=1)
    ])
    triangle_segments.append([  # Right
        Curve(np.asfortranarray([[square_size, square_size/2], [square_size, square_size]]), degree=1),
        Curve(np.asfortranarray([[square_size/2, square_size], [square_size, 0.0]]), degree=1),
        Curve(np.asfortranarray([[square_size, square_size], [0.0, square_size]]), degree=1)
    ])

    # Now let's create the upside down triangle shaped gaps
    def add_triangle_gap(bottom_left, square_size):
        triangle_segments.append([
            Curve(np.asfortranarray([
                [bottom_left[0]+(1/4)*square_size, bottom_left[0]+(3/4)*square_size],
                [bottom_left[1]+(1/2)*square_size, bottom_left[1]+(1/2)*square_size]
            ]), degree=1),
            Curve(np.asfortranarray([
                [bottom_left[0]+(3/4)*square_size, bottom_left[0]+(1/2)*square_size],
                [bottom_left[1]+(1/2)*square_size, bottom_left[1]]
            ]), degree=1),
            Curve(np.asfortranarray([
                [bottom_left[0]+(1/2)*square_size, bottom_left[0]+(1/4)*square_size],
                [bottom_left[1], bottom_left[1]+(1/2)*square_size]
            ]), degree=1),
        ])

    def subdivide_square(bottom_left, square_size):
        """Returns the bottom lefts of the next three squares"""
        return [
            bottom_left,
            (bottom_left[0]+square_size/2, bottom_left[1],),
            (bottom_left[0]+square_size/4, bottom_left[1]+square_size/2,)
        ]
    
    square_bottom_lefts = [(0,0)]
    cur_square_size = square_size
    
    for i in range(num_iterations):
        for bottom_left in square_bottom_lefts:
            add_triangle_gap(bottom_left, cur_square_size)
        
        if i != (num_iterations - 1):
            square_bottom_lefts = [bl for old_bl in square_bottom_lefts for bl in subdivide_square(old_bl, cur_square_size)]
            cur_square_size = cur_square_size/2

    # Now let's paint the non-gaps
    # This will require a different approach
    # Here we first generate all of the curve points, then create the curves
    cur_square_size = square_size/(2**num_iterations)

    non_gap_curves = [
        ([0.0, cur_square_size, cur_square_size/2], [0.0, 0.0, cur_square_size])      # We'll split this curve up later
    ]

    def duplicate(existing_curves, new_square_size):
        """Assumes the existing curves are on the bottom left corner of the new square"""
        new_curves = []
        for curve in existing_curves:
            new_curves.append(([x + new_square_size/2 for x in curve[0]], [y for y in curve[1]]))
            new_curves.append(([x+new_square_size/4 for x in curve[0]], [y + new_square_size/2 for y in curve[1]]))
        
        return existing_curves + new_curves

    for i in range(num_iterations):
        cur_square_size = cur_square_size * 2
        non_gap_curves = duplicate(non_gap_curves, cur_square_size)

    triangle_segments = triangle_segments + [[
        Curve(np.asfortranarray([[c[0][0], c[0][1]], [c[1][0], c[1][1]]]), degree=1),
        Curve(np.asfortranarray([[c[0][1], c[0][2]], [c[1][1], c[1][2]]]), degree=1),
        Curve(np.asfortranarray([[c[0][2], c[0][0]], [c[1][2], c[1][0]]]), degree=1),
        ] for c in non_gap_curves]

    return triangle_segments


    