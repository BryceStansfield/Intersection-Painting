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
        

        


