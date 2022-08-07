import Painter
import Grids
import matplotlib.pyplot as plt
import numpy as np
import bezier
import Curves
import Animations

test_grid = Grids.sierpinski_triangle(6, 1)
NUM_FRAMES = 100

animation = Animations.ball_bounce(0.1, (0.5, 0.5), (0.05, 0), 0.05, 0.01, 0.9, NUM_FRAMES)

for i in range(NUM_FRAMES):
    fig = plt.figure()
    fig.set_figwidth(10)
    fig.set_figheight(10)
    ax = fig.add_subplot(1,1,1)
    ax.axis('tight')
    ax.axis('off')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    intersected_grid_cells = Painter.find_intersecting_polygons(test_grid, animation[i])
    #print(len(test_grid), len(intersected_grid_cells))
    Painter.paint_polygons(ax, intersected_grid_cells, color=(0,0,0,))
    #Painter.paint_polygons(ax, test_grid, color=(0,0,0,))

    plt.savefig("outputs/WithoutCurve/{:03}.png".format(i))
    for curve in animation[i]:
        curve.plot(100, (0,0,0), ax=ax)
    
    plt.savefig("outputs/WithCurve/{:03}.png".format(i))
    fig.gca().cla()
