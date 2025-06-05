# scripts/main.py

# การ import แบบนี้จะทำงานได้ถูกต้องเมื่อเราติดตั้งโปรเจกต์ด้วย 'pip install -e .'
from pathfinder import parse_image_to_grid, find_path_bfs, display_result

def run_pathfinder():
    """The main function to run the pathfinding process."""
    IMAGE_FILE = "map.png"
    print(f"Processing '{IMAGE_FILE}'...")

    try:
        grid_data, red_points = parse_image_to_grid(IMAGE_FILE)
    except FileNotFoundError as e:
        print(e)
        print("Hint: You can create a sample map by running the 'createmap' command.")
        return  # จบการทำงาน

    if grid_data is not None and red_points is not None:
        start_point, end_point = red_points[0], red_points[1]
        print(f"Scan complete. Start: {start_point}, End: {end_point}")

        print("Finding path using BFS...")
        found_path = find_path_bfs(grid_data, start_point, end_point)

        if found_path:
            print(f"Path found! Length: {len(found_path) - 1} steps.")
        else:
            print("Could not find a path.")

        display_result(grid_data, start_point, end_point, found_path)


if __name__ == "__main__":
    run_pathfinder()