from bezier import Curve
import Curves

def ball_bounce(ball_radius, ball_start, start_velocity, gravity, drag, bounce_ratio, frames) -> list[list[Curve]]:
    """List of curves corrosponding to a ball with radius `ball_radius` starting at position `ball_start` with velocity `start_velocity`
    drag factor `drag` and gravity factor `gravity` bouncing for `frames` frames"""
    cur_pos = (ball_start[0], ball_start[1],)
    ball_centres = [cur_pos]
    velocity = start_velocity

    for _ in range(frames-1):
        # Updating x
        cur_pos = (cur_pos[0] + velocity[0], cur_pos[1] + velocity[1],)

        if cur_pos[1] < ball_radius:
            cur_pos = (cur_pos[0], (ball_radius - cur_pos[1]) + ball_radius,)
            velocity = (velocity[0], -velocity[1] * bounce_ratio,)
        
        if cur_pos[0] < ball_radius:
            cur_pos = ((ball_radius - cur_pos[0]) + ball_radius, cur_pos[1],)
            velocity = (-velocity[0], velocity[1],)
        elif cur_pos[0] > 1-ball_radius:
            cur_pos = ((1-ball_radius) - (cur_pos[0] - (1-ball_radius)), cur_pos[1],)
            velocity = (-velocity[0], velocity[1],)
        ball_centres.append(cur_pos)
        
        # Updating x'
        velocity = ((1-drag)*velocity[0], (1-drag)*velocity[1] - gravity,)

    return [Curves.approximate_circle(centre, ball_radius) for centre in ball_centres]
        

def pulsating_circles(frame_size, start_position, delta_radius, start_radius, frames_per_circle, num_frames) -> list[list[Curve]]:
    """num_frames-Animation of pulsating circles from the centre of the frame (of size frame_size = (x,y,)), one new circle every `frames_per_circle` with start radius start_radius"""
    frames = []
    cur_circles = []
    
    circle_ttl = 1

    for _ in range(num_frames):
        # Expanding existing circles
        cur_circles = [c + delta_radius for c in cur_circles]
        while len(cur_circles) > 0 and cur_circles[0] > max(max(frame_size[0]-start_position[0], start_position[0]), max(frame_size[1]-start_position[1], start_position[1]))/2:
            cur_circles.pop(0)   # Almost certainly inefficient, but it shouldn't matter too much

        # New circles
        circle_ttl -= 1
        if circle_ttl == 0:
            cur_circles.append(start_radius)
            circle_ttl = frames_per_circle

        # Render circles
        frames.append(sum([Curves.approximate_circle(start_position, c) for c in cur_circles], start=[]))
    
    return frames

def combine_animations(*anims) -> list[list[Curve]]:
    return [sum(curve_sets, start=[]) for curve_sets in zip(*anims)]
