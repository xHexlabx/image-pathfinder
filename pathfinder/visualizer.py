# pathfinder/visualizer.py

import numpy as np
import matplotlib.pyplot as plt
from . import config


def display_result(grid, start, end, path):
    """Displays the grid, start/end points, and the found path using Matplotlib."""
    display_img = np.full((*grid.shape, 3), config.COLOR_WHITE, dtype=np.uint8)
    display_img[grid == 1] = config.COLOR_BLACK
    display_img[start] = config.COLOR_GREEN_START
    display_img[end] = config.COLOR_PURPLE_END

    if path:
        for y, x in path[1:-1]:  # Draw path without overwriting start/end points
            display_img[y, x] = config.COLOR_BLUE_PATH

    fig, ax = plt.subplots(1)
    ax.imshow(display_img)
    ax.set_xticks(np.arange(-.5, config.GRID_SIZE, 1), minor=True)
    ax.set_yticks(np.arange(-.5, config.GRID_SIZE, 1), minor=True)
    ax.grid(which="minor", color="k", linestyle='-', linewidth=1)
    ax.tick_params(which="minor", size=0)
    ax.set_xticks([])
    ax.set_yticks([])

    title = "Path Found!" if path else "No Path Found"
    plt.title(title)
    plt.show()