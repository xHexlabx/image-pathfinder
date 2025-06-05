# pathfinder/image_handler.py

import os
import numpy as np
from PIL import Image, ImageDraw
from . import config


def generate_sample_grid_image(filename="map.png"):
    """Generates and saves a sample 10x10 grid image."""
    layout = [
        ['R', 'W', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'W'],
        ['W', 'B', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W'],
        ['W', 'B', 'W', 'B', 'W', 'W', 'W', 'B', 'B', 'W'],
        ['W', 'B', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'W'],
        ['W', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'B'],
        ['B', 'B', 'B', 'W', 'B', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'R'],
    ]
    img = Image.new('RGB', config.IMAGE_SIZE, config.COLOR_WHITE)
    draw = ImageDraw.Draw(img)
    color_map = {'W': config.COLOR_WHITE, 'B': config.COLOR_BLACK, 'R': config.COLOR_RED}
    for y, row in enumerate(layout):
        for x, cell_type in enumerate(row):
            top_left = (x * config.CELL_SIZE, y * config.CELL_SIZE)
            bottom_right = ((x + 1) * config.CELL_SIZE, (y + 1) * config.CELL_SIZE)
            draw.rectangle([top_left, bottom_right], fill=color_map[cell_type])
    img.save(filename)
    print(f"Sample map image '{filename}' created successfully.")


def parse_image_to_grid(filename="map.png"):
    """Reads an image file and converts it into a 2D grid representation."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Map file not found: '{filename}'. Please create it first.")

    img = Image.open(filename).convert('RGB').resize(config.IMAGE_SIZE)
    grid = np.zeros((config.GRID_SIZE, config.GRID_SIZE), dtype=int)
    red_points = []

    for y in range(config.GRID_SIZE):
        for x in range(config.GRID_SIZE):
            px_x = x * config.CELL_SIZE + (config.CELL_SIZE // 2)
            px_y = y * config.CELL_SIZE + (config.CELL_SIZE // 2)
            r, g, b = img.getpixel((px_x, px_y))

            if abs(r - config.COLOR_RED[0]) < 50 and abs(g - config.COLOR_RED[1]) < 50 and abs(
                    b - config.COLOR_RED[2]) < 50:
                grid[y, x] = 0
                red_points.append((y, x))
            elif abs(r - config.COLOR_BLACK[0]) < 50 and abs(g - config.COLOR_BLACK[1]) < 50 and abs(
                    b - config.COLOR_BLACK[2]) < 50:
                grid[y, x] = 1
            else:
                grid[y, x] = 0

    if len(red_points) != 2:
        print(f"Error: Found {len(red_points)} red points, but expected 2.")
        return None, None
    return grid, red_points