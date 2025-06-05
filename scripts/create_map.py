# scripts/create_map.py

import argparse
# เราจะ import ทั้งสองฟังก์ชันมาเพื่อเลือกใช้
from pathfinder.image_handler import generate_static_map_image, generate_random_map_image


def main():
    """Script entry point for creating a map."""
    parser = argparse.ArgumentParser(description="Generate a map image for the pathfinder.")

    # --- Arguments for both modes ---
    parser.add_argument("-o", "--output", default="map.png", help="Output filename (default: map.png)")

    # --- Switch between random and static ---
    parser.add_argument("--random", action="store_true", help="Generate a random map instead of the static one.")

    # --- Arguments for random mode ---
    parser.add_argument("--density", type=float, default=0.25,
                        help="Wall density for random maps (0.0 to 1.0). Default is 0.25.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Seed for the random number generator for reproducible maps.")
    parser.add_argument("--unsolvable", action="store_true",
                        help="Allow the creation of random maps that might not have a solution.")

    args = parser.parse_args()

    if args.random:
        # โหมดสุ่ม
        generate_random_map_image(
            filename=args.output,
            wall_density=args.density,
            ensure_solvable=not args.unsolvable,
            seed=args.seed
        )
    else:
        # โหมดปกติ (แผนที่ตายตัว)
        generate_static_map_image(filename=args.output)


if __name__ == "__main__":
    main()