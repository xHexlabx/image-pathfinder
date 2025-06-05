# scripts/create_map.py

import argparse
# การ import แบบนี้จะทำงานได้ถูกต้องเมื่อเราติดตั้งโปรเจกต์ด้วย 'pip install -e .'
from pathfinder.image_handler import generate_sample_grid_image


def main():
    """Script entry point for creating a sample map."""
    parser = argparse.ArgumentParser(description="Generate a sample map image for the pathfinder.")
    parser.add_argument(
        "-o", "--output",
        default="map.png",
        help="Output filename for the map image (default: map.png)"
    )
    args = parser.parse_args()

    generate_sample_grid_image(args.output)


if __name__ == "__main__":
    main()