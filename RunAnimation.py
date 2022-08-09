import Painter
import Grids
import matplotlib.pyplot as plt
import numpy as np
import bezier
import Curves
from Common import FakePolygonCollection
import Animations
import os

def run_animation(animation: list[list[bezier.Curve]], grid: list[FakePolygonCollection], withoutCurveFolder=None, withCurveFolder=None):
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

        intersected_grid_cells = Painter.find_intersecting_polygons(grid, frame)
        Painter.paint_polygons(ax, intersected_grid_cells, color=(0,0,0,))

        plt.savefig(f"outputs/{withoutCurveFolder}/" + "{:06}.png".format(i))       # TODO: Adjust decimal format based on |FRAMES|

        for curve in frame:
            curve.plot(100, (0,0,0), ax=ax)
        plt.savefig(f"outputs/{withCurveFolder}/" + "{:06}.png".format(i))
        plt.close(fig)
        
#run_animation(Animations.ball_bounce(0.1, (0.5, 0.5), (0.05, 0), 0.02, 0.01, 0.9, 300), Grids.sierpinski_triangle(6, 1), "WithoutCurve", "WithCurve")
run_animation(Animations.pulsating_circles((1,1,), (0.5,0.5,), 0.02, 0.02, 15, 300), Grids.sierpinski_triangle(6, 1), "WithoutCurveOnCentre", "WithCurveOnCentre")
run_animation(Animations.pulsating_circles((1,1,), (0,0,), 0.02, 0.02, 15, 300), Grids.sierpinski_triangle(6, 1), "WithoutCurveOnCorner", "WithCurveOnCorner")