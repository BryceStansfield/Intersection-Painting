from bezier import Curve
import Curves
import Common
import math

def ball_bounce(ball_radius, ball_start, start_velocity, gravity, drag, bounce_ratio, frames) -> list[list[Common.Collider]]:
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

    return [[Common.Collider(Curves.approximate_circle(centre, ball_radius))] for centre in ball_centres]
        

def pulsating_circles(frame_size, start_position, delta_radius, start_radius, frames_per_circle, num_frames, colours = [(0,0,0,)], patterns=[Curves.approximate_circle]) -> list[list[Common.Collider]]:
    """num_frames-Animation of pulsating circles from the centre of the frame (of size frame_size = (x,y,)), one new circle every `frames_per_circle` with start radius start_radius.
       Cycles through `colours`"""
    frames = []
    cur_circles = []
    cur_circles_indicies = []
    
    circle_ttl = 1
    next_circle_i = 0

    end_radius = max(*[math.dist(start_position, (x, y)) for x in (0, frame_size[0]) for y in (0, frame_size[1])]) + 0.1

    for _ in range(num_frames):
        # Expanding existing circles
        cur_circles = [c + delta_radius for c in cur_circles]
        while len(cur_circles) > 0 and cur_circles[0] > end_radius:
            cur_circles.pop(0)   # Almost certainly inefficient, but it shouldn't matter too much
            cur_circles_indicies.pop(0)

        # New circles
        circle_ttl -= 1
        if circle_ttl == 0:
            cur_circles.append(start_radius)
            cur_circles_indicies.append(next_circle_i)
            next_circle_i += 1
            circle_ttl = frames_per_circle

        # Render circles
        frames.append([Common.Collider(patterns[cur_circles_indicies[i] % len(patterns)](start_position, c), colour=colours[cur_circles_indicies[i] % len(colours)]) for i, c in enumerate(cur_circles)])
    
    return frames

def combine_animations(*anims) -> list[list[Common.Collider]]:
    return [sum(curve_sets, start=[]) for curve_sets in zip(*anims)]
