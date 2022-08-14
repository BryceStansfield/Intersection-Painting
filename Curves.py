import pdb
from bezier import Curve, CurvedPolygon
import numpy as np
import math

# A collection of curve generating functions, for testing things out on
# Tools
def get_point(angle, length, centre):
    return (math.cos(angle)*length+centre[0], math.sin(angle)*length+centre[1],)

def stretch_curve_radially(curve: Curve, centre: tuple[float, float], expansion_factor: float) -> Curve:
    nodes = curve.nodes
    new_curve_points = [[], []]

    for i in range(nodes.shape[1]):
        normalized_point = (nodes[0][i]-centre[0], nodes[1][i]-centre[1],)
        point_length = math.sqrt(normalized_point[0]**2 + normalized_point[1]**2)
        point_angle = math.atan2(normalized_point[1], normalized_point[0])

        new_point = get_point(point_angle, point_length*expansion_factor, centre)
        new_curve_points[0].append(new_point[0])
        new_curve_points[1].append(new_point[1])

    return Curve(new_curve_points, degree=curve.degree)

def shift_curve(curve: Curve, shift: tuple[float, float]) -> Curve:
    nodes = curve.nodes
    new_curve_points = [[], []]

    for i in range(nodes.shape[1]):
        new_curve_points[0].append(nodes[0][i] + shift[0])
        new_curve_points[1].append(nodes[1][i] + shift[1])

    return Curve(new_curve_points, degree=curve.degree)

def linear_curves_from_points(points: list[tuple[float, float]]) -> list[Curve]:
    return [Curve([[points[i][0], points[i+1][0]],[points[i][1], points[i+1][1]]], degree=1) for i in range(len(points)-1)]

def inscribe_in_square(curvedPolygon: CurvedPolygon, centre: tuple[float, float], side_length: float, clockwise) -> list[CurvedPolygon]:
    """Radilly inscribes a curved polygon inside of a square, will only work if the base curved_polygon is close enough to convex I think?
        Each segment is turned into a seperate curvedPolygon
    TODO: Currently only works with clockwise curves :'(, I need to fix that
    NOTE 2: This is broken, and contains some funny shapes, it also doesn't work well for the cat so I don't feel like working on it any more"""

    def get_square_segment(start_point: tuple[float, float], end_point: tuple[float, float]) -> list[Curve]:
        # Assumes start_point comes before end_point counter-clockwise
        def normalize_angle(angle: float):
            while angle > 2 * math.pi:
                angle -= 2 * math.pi
            while angle < 0:
                angle += 2 * math.pi
            
            return angle
        
        def get_corner_after(angle: float):
            """Gets the next corner after `angle`, in the counter-clockwise direction"""
            angle = normalize_angle(angle)
            
            half_length = side_length/2
            if angle < (1/4) * math.pi:
                return (centre[0] + half_length, centre[1] + half_length), (1/4) * math.pi
            if angle < (3/4) * math.pi:
                return (centre[0] - half_length, centre[1] + half_length), (3/4) * math.pi
            if angle < (5/4) * math.pi:
                return (centre[0] - half_length, centre[1] - half_length), (5/4) * math.pi
            if angle < (7/4) * math.pi:
                return (centre[0] + half_length, centre[1] - half_length), (7/4) * math.pi
            return (centre[0] + half_length, centre[1] + half_length), (1/4) * math.pi
            
        
        def get_rectangle_point_at(angle: float):
            """Gets the rectangle point corrosponding to `angle`"""
            next_corner, _ = get_corner_after(angle)
            last_corner, _ = get_corner_after(angle - math.pi/2)
            alpha = ((angle + math.pi/4) % (math.pi/2))/(math.pi/2) # TODO: Something is wrong with this formula.

            return (next_corner[0] * alpha + last_corner[0] * (1 - alpha), next_corner[1] * alpha + last_corner[1] * (1 - alpha))
        
        def num_corners_between(start_angle: float, end_angle: float):
            """Returns the number of corners between start_angle and end_angle
               Assumes end_angle > start_angle"""
               
            angle_dist = end_angle - start_angle
            dist_to_first_corner = math.pi/2 - ((start_angle + math.pi/4) % math.pi/2)
            
            if dist_to_first_corner < angle_dist:
                angle_dist -= dist_to_first_corner
                return math.floor(angle_dist/(math.pi/2)) + 1
            return 0
        
        # We flip the start and end point for clockwise curves
        if clockwise:
            start_point, end_point = end_point, start_point
        
        start_angle = math.atan2(start_point[1] - centre[1], start_point[0] - centre[0])
        end_angle = math.atan2(end_point[1] - centre[1], end_point[0] - centre[0])
        while end_angle < start_angle:
            end_angle += 2 * math.pi

        # Generating point connecting to and on the square
        last_angle = start_angle
        point_list = [start_point, get_rectangle_point_at(start_angle)]

        for _ in range(num_corners_between(start_angle, end_angle)):
            last_point, last_angle = get_corner_after(last_angle)
            point_list.append(last_point)
        point_list.append(get_rectangle_point_at(end_angle))
        point_list.append(end_point)

        # For counter-clockwise curves we need to swap the direction of the point_list before returning.
        if not clockwise:
            point_list.reverse()

        return linear_curves_from_points(point_list)
    
    ret_polygons = [curvedPolygon]
    for edge in curvedPolygon._edges:
        points = edge._nodes
        if not clockwise:
            square_segment = get_square_segment((points[0][0], points[1][0]), (points[0][-1], points[1][-1]))
            square_segment.reverse()
            ret_polygons.append(CurvedPolygon(edge, *square_segment))
        else:
            ret_polygons.append(CurvedPolygon(edge, *get_square_segment((points[0][0], points[1][0]), (points[0][-1], points[1][-1]))))
    
    return ret_polygons


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

def generate_cat_outline(centre: tuple[float, float], radius: float) -> list[Curve]:
    base_radius = 0.4

    """ OLD counterclockwise curve
    # Head Curve
    curve1 = Curve(np.asfortranarray([[0.25, 0.5, 0.25], [0.2, 0, -0.2]]), degree=2)
    curve2 = Curve(np.asfortranarray([[0.25, 0, -0.25], [-0.2, -0.35, -0.2]]), degree=2)
    #curve2 = Curve(np.asfortranarray([[0.25, 0.125, 0], [-0.2, -0.25, -0.28]]), degree=2)
    curve3 = Curve(np.asfortranarray([[-0.25, -0.5, -0.25], [-0.2, 0, 0.2]]), degree=2)
    #curve4 = Curve(np.asfortranarray([[-0.25, -0.125, 0], [-0.2, -0.25, -0.28]]), degree=2)
    
    # Ears and scalp
    ear_height = 0.4
    curve5 = Curve(np.asfortranarray([[-0.25, -0.2], [0.2, ear_height]]), degree=1)
    curve6 = Curve(np.asfortranarray([[-0.2, -0.15], [ear_height, 0.24]]), degree=1)
    curve7 = Curve(np.asfortranarray([[-0.15, 0.0, 0.15], [0.24, 0.3, 0.24]]), degree=2)
    curve8 = Curve(np.asfortranarray([[0.15, 0.2], [0.24, ear_height]]), degree=1)
    curve9 = Curve(np.asfortranarray([[0.2, 0.25], [ear_height, 0.20]]), degree=1)
    curves = [curve1, curve2, curve3, curve5, curve6, curve7, curve8, curve9]"""
    # Ears and scalp
    ear_height = 0.4
    curve1 = Curve(np.asfortranarray([[0.25, 0.2], [0.2, ear_height]]), degree=1)
    curve2 = Curve(np.asfortranarray([[0.2, 0.15], [ear_height, 0.24]]), degree=1)
    curve3 = Curve(np.asfortranarray([[0.15, 0.0, -0.15], [0.24, 0.3, 0.24]]), degree=2)
    curve4 = Curve(np.asfortranarray([[-0.15, -0.2], [0.24, ear_height]]), degree=1)
    curve5 = Curve(np.asfortranarray([[-0.2, -0.25], [ear_height, 0.2]]), degree=1)

    curve6 = Curve(np.asfortranarray([[-0.25, -0.5, -0.25], [0.2, 0, -0.2]]), degree=2)
    curve7 = Curve(np.asfortranarray([[-0.25, 0, 0.25], [-0.2, -0.35, -0.2]]), degree=2)
    curve8 = Curve(np.asfortranarray([[0.25, 0.5, 0.25], [-0.2, 0, 0.2]]), degree=2)
    curves = [curve1, curve2, curve3, curve4, curve5, curve6, curve7, curve8]

    return [stretch_curve_radially(shift_curve(c, centre), centre, radius/base_radius) for c in curves]

def generate_circle_segments(start_angle, end_angle, radius, centre) -> list[Curve]:
    """generate_circle_segment except it support large angles and returns a list of curves instead of a single curve"""
    # TODO: Test
    while end_angle < start_angle:
        end_angle += 360
    
    angle_diff = end_angle - start_angle

    segments = []
    for i in range(math.ceil(angle_diff/90)):
        segments.append(generate_circle_segment(start_angle + i * 90, min(end_angle, start_angle + (i+1)*90), radius, centre))
    
    return segments

def generate_circle_segment(start_angle, end_angle, radius, centre) -> Curve:
    """Generates an approximate circle segment of radius radius from start_angle to end_angle centred at centre"""
    # See: https://math.stackexchange.com/questions/873224/calculate-control-points-of-cubic-bezier-curve-approximating-a-part-of-a-circle

    # Figuring out theta
    if end_angle > start_angle:
        theta = end_angle - start_angle
    else:
        theta = end_angle - start_angle + 2*math.pi
    
    # Figuring out alpha
    alpha = (4/3)*math.tan(theta)

    # Generating centred curve, with start_angle = 0
    virtual_control_point = (alpha*radius, radius)
    control_point_dist = math.sqrt(virtual_control_point[0]**2 + virtual_control_point[1]**2)
    control_point_angle_diff = math.atan2(virtual_control_point[1], virtual_control_point[0])

    def generate_point(angle, dist):
        return (math.sin(angle)*dist + centre[0], math.cos(angle)*dist + centre[1],)
    start_point = generate_point(start_angle, radius)
    control_point_1 = generate_point(start_angle + control_point_angle_diff, control_point_dist)
    control_point_2 = generate_point(end_angle - control_point_angle_diff, control_point_dist)
    end_point = generate_point(end_angle, radius)

    return Curve([[start_point[0], control_point_1[0], control_point_2[0], end_point[0]], [start_point[1], control_point_1[1], control_point_2[1], end_point[1]]], degree=3)