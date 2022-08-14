import Painter
import Grids
import matplotlib.pyplot as plt
import numpy as np
import bezier
import Curves
from Common import FakePolygonCollection, Collider
import Animations
import os

def run_animation(animation: list[list[Collider]], grid: list[FakePolygonCollection], grid_size: tuple[float, float], withoutCurveFolder=None, withCurveFolder=None):
    def create_folder_if_not_exists(folder):
        """Note: This will fail if `folder` exists as a file in outputs, or if `outputs` exists as a file, but this is a hobby project so I don't particularly much care"""
        if not os.path.exists("outputs"):
            os.mkdir("outputs")

        if not os.path.exists(f"outputs/{folder}"):
            os.mkdir(f"outputs/{folder}")

    create_folder_if_not_exists(withoutCurveFolder)
    create_folder_if_not_exists(withCurveFolder)

    for i, frame in enumerate(animation):
        fig = plt.figure()
        fig.set_figwidth(10)
        fig.set_figheight(10)
        ax = fig.add_subplot(1,1,1)
        ax.axis('tight')
        ax.axis('off')
        plt.xlim(0, 1)
        plt.ylim(0, 1)

        Painter.paint_intersecting_polygons(ax, grid, grid_size, frame)
        #intersected_grid_cells = Painter.find_intersecting_polygons(grid, frame)
        #Painter.paint_polygons(ax, intersected_grid_cells, color=(0,0,0,))

        plt.savefig(f"outputs/{withoutCurveFolder}/" + "{:06}.png".format(i))       # TODO: Adjust decimal format based on |FRAMES|

        for collider in frame:
            for curve in collider.curves:
                curve.plot(100, collider.colour, ax=ax)         # TODO: Colour line correctly
        plt.savefig(f"outputs/{withCurveFolder}/" + "{:06}.png".format(i))
        plt.close(fig)
        
#run_animation(Animations.ball_bounce(0.01, (0.5, 0.5), (0.05, 0), 0.02, 0.01, 0.9, 300), Grids.sierpinski_triangle(6, 1), (1,1,), "WithoutCurve", "WithCurve")
#run_animation(Animations.pulsating_circles((1,1,), (0.5,0.5,), 0.02, 0.02, 15, 300, colours=[(1,0,0,), (0,1,0,), (0,0,1,)]), Grids.sierpinski_triangle(6, 1), (1,1,), "WithoutCurveOnCentre", "WithCurveOnCentre")
#run_animation(Animations.pulsating_circles((1,1,), (0,0,), 0.02, 0.02, 15, 300, colours=[(1,0,0,), (0,1,0,), (0,0,1,)]), Grids.sierpinski_triangle(6, 1), (1,1,), "WithoutCurveOnCorner", "WithCurveOnCorner")
run_animation(Animations.pulsating_circles((1,1,), (0.5,0.5,), 0.02, 0.02, 15, 300, colours=[(1,0,0,), (0,1,0,), (0,0,1,)], patterns=[Curves.generate_cat_outline]), Grids.sierpinski_triangle(6, 1), (1,1,), "WithoutCurveRainbowCats", "WithCurveRainbowCats")