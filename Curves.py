from bezier import Curve
import numpy as np
import math

# A collection of curve generating functions, for testing things out on
def rectangle(bottom_left, size) -> list[Curve]:
    """bottom_left(x,y), size(width, height)"""
    start_x = bottom_left[0]
    end_x = bottom_left[0] + size[0]
    start_y = bottom_left[1]
    end_y = bottom_left[1] + size[1]

    return ([
        Curve(np.asfortranarray([[start_x, start_x], [start_y, end_y]])),
        Curve(np.asfortranarray([[start_x, end_x], [end_y, end_y]])),
        Curve(np.asfortranarray([[end_x, end_x], [end_y, start_y]])),
        Curve(np.asfortranarray([[end_x, start_x], [start_y, start_y]]))
    ])


def approximate_circle(centre, radius) -> list[Curve]:
    """Gets all four points for a curve segment starting at theta on a unit circle
        These are returned in the right shape
    centre = (x,y)"""
    # See https://stackoverflow.com/questions/1734745/how-to-create-circle-with-b%C3%A9zier-curves#:~:text=A%20common%20approximation%20is%20to,circle%20at%20the%20end%20points. for methodology
    def control_point_at(p, is_clockwise):
        distance = (4/3)*math.tan(math.pi/8)
        if p == (1, 0):
            return (1, (-1 if is_clockwise else 1) * distance)
        if p == (-1, 0):
            return (-1, (1 if is_clockwise else -1) * distance)
        if p == (0, 1):
            return ((1 if is_clockwise else -1) * distance, 1)
        if p == (0, -1):
            return ((-1 if is_clockwise else 1) * distance, -1)

        raise Exception("Invalid p")
    
    def uc_to_circle(point):
        """Converts a unit circle point to a point on the finished circle"""
        return (point[0]*radius+centre[0], point[1]*radius+centre[1])

    def generate_curves():
        """ Generates the curve_points for a unit circle """
        start_points = [(1,0), (0, -1), (-1, 0), (0, 1)]
        curves = [] # In the shape of the final fortran array
        for i in range(len(start_points)):
            start_point = uc_to_circle(start_points[i])
            end_point = uc_to_circle(start_points[(i+1)%4])
            control_point_1 = uc_to_circle(control_point_at(start_points[i], True))
            control_point_2 = uc_to_circle(control_point_at(start_points[(i+1)%4], False))

            curves.append(
                Curve(
                    np.asfortranarray([[start_point[0], control_point_1[0], control_point_2[0], end_point[0]],
                    [start_point[1], control_point_1[1], control_point_2[1], end_point[1]]]), degree=3
                )
            )
        
        return curves
    
    return generate_curves()
