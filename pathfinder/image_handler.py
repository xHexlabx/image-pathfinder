# pathfinder/image_handler.py

import os
import random
import numpy as np
from PIL import Image, ImageDraw
from . import config
# ▼▼▼ ใหม่: import อัลกอริทึมของเรามาใช้เพื่อเช็คว่าแผนที่แก้ได้หรือไม่ ▼▼▼
from .algorithm import find_path_bfs


def _draw_layout_to_image(layout, filename):
    """Internal helper to draw a given layout and save it as an image."""
    img = Image.new('RGB', config.IMAGE_SIZE, config.COLOR_WHITE)
    draw = ImageDraw.Draw(img)
    color_map = {'W': config.COLOR_WHITE, 'B': config.COLOR_BLACK, 'R': config.COLOR_RED}
    for y, row in enumerate(layout):
        for x, cell_type in enumerate(row):
            top_left = (x * config.CELL_SIZE, y * config.CELL_SIZE)
            bottom_right = ((x + 1) * config.CELL_SIZE, (y + 1) * config.CELL_SIZE)
            draw.rectangle([top_left, bottom_right], fill=color_map[cell_type])
    img.save(filename)


def generate_static_map_image(filename="map.png"):
    """Generates and saves a static, predefined 10x10 grid image."""
    layout = [
        ['R', 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],
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
    _draw_layout_to_image(layout, filename)
    print(f"Static map image '{filename}' created successfully.")


def generate_random_map_image(filename="map.png", wall_density=0.25, ensure_solvable=True, seed=None):
    """Generates and saves a random 10x10 grid image."""
    if seed:
        random.seed(seed)

    print("Generating random map... (this may take a moment if ensure_solvable=True)")

    while True:
        # 1. สร้างแผนที่กำแพงแบบสุ่ม
        layout = [['W' if random.random() > wall_density else 'B' for _ in range(config.GRID_SIZE)] for _ in
                  range(config.GRID_SIZE)]

        # 2. หาตำแหน่งที่เป็นทางเดินทั้งหมดเพื่อสุ่มจุดเกิด
        walkable_tiles = []
        for r, row in enumerate(layout):
            for c, tile in enumerate(row):
                if tile == 'W':
                    walkable_tiles.append((r, c))

        # 3. ถ้ามีทางเดินน้อยกว่า 2 จุด ให้สุ่มใหม่
        if len(walkable_tiles) < 2:
            continue

        # 4. สุ่มเลือก 2 จุดสำหรับเริ่มต้นและสิ้นสุด
        start_pos, end_pos = random.sample(walkable_tiles, 2)

        # 5. ตรวจสอบว่าแผนที่นี้แก้ได้หรือไม่ (ถ้าเปิดใช้งาน)
        if ensure_solvable:
            # สร้าง grid สำหรับ BFS check (0=ทางเดิน, 1=กำแพง)
            grid_for_check = np.array([[0 if cell == 'W' else 1 for cell in row] for row in layout])
            if find_path_bfs(grid_for_check, start_pos, end_pos):
                # ถ้าหาเจอ, วางจุด 'R' แล้วออกจากลูป
                layout[start_pos[0]][start_pos[1]] = 'R'
                layout[end_pos[0]][end_pos[1]] = 'R'
                break
                # ถ้าหาไม่เจอ, ลูปจะทำงานต่อไปเพื่อสุ่มแผนที่ใหม่
        else:
            # ถ้าไม่ต้องการเช็ค, วางจุด 'R' แล้วออกจากลูปเลย
            layout[start_pos[0]][start_pos[1]] = 'R'
            layout[end_pos[0]][end_pos[1]] = 'R'
            break

    # 6. วาดแผนที่ที่สมบูรณ์ลงไฟล์
    _draw_layout_to_image(layout, filename)
    solvability = "solvable" if ensure_solvable else "potentially unsolvable"
    print(f"Random ({solvability}) map image '{filename}' created successfully.")


# ฟังก์ชัน parse_image_to_grid() ยังคงเหมือนเดิม ไม่ต้องแก้ไข
def parse_image_to_grid(filename="map.png"):
    """Reads an image file and converts it into a 2D grid representation."""
    # ... (โค้ดเหมือนเดิมทุกประการ) ...
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