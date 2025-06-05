# pathfinder/__init__.py

# Make key functions available directly from the package
from .image_handler import parse_image_to_grid
from .algorithm import find_path_bfs
from .visualizer import display_result