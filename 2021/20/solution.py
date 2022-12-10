from __future__ import annotations
import sys
import time

infinite_pixel = '.'
PART_1_ENHANCEMENTS: int = 2
PART_2_ENHANCEMENTS: int = 50

def get_neighbors_as_binary(grid: dict, x: int, y: int):
    neighbors = [grid.get((x-1, y-1), infinite_pixel), grid.get((x, y-1), infinite_pixel), grid.get((x+1, y-1), infinite_pixel),
            grid.get((x-1, y), infinite_pixel), grid.get((x, y), infinite_pixel), grid.get((x+1, y), infinite_pixel),
            grid.get((x-1, y+1), infinite_pixel), grid.get((x, y+1), infinite_pixel), grid.get((x+1, y+1), infinite_pixel)]
    return ''.join(['0' if pixel == '.' else '1' for pixel in neighbors])

def enhance_grid(pixels: dict, enhancement_algo, min_coord: tuple, max_coord: tuple):
    new_pixels = dict()
    for y in range(min_coord[1], max_coord[1]):
        for x in range(min_coord[0], max_coord[0]):
            new_pixels[(x,y)] = enhancement_algo[int(get_neighbors_as_binary(pixels, x, y), 2)]
    return new_pixels

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    enhancement_algo = None
    pixels = dict()
    min_coord = (0,0)
    max_coord = (0,0)

    with open(filename) as f:
        lines = f.read().splitlines()
        enhancement_algo = lines[0]
        y: int = 0
        for line in lines[2:]:
            max_coord = (len(line)-1, y)
            for x in range(len(line)):
                pixels[(x,y)] = line[x]
            y += 1

    for i in range(PART_1_ENHANCEMENTS):
        infinite_pixel = enhancement_algo[0] if i % 2 == 1 else '.'
        min_coord = (min_coord[0]-2, min_coord[1]-2)
        max_coord = (max_coord[0]+2, max_coord[1]+2)
        pixels = enhance_grid(pixels, enhancement_algo, min_coord, max_coord)

    result = sum([1 if pixel == '#' else 0 for pixel in pixels.values()])
    print(f"Part 1: {result} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    for i in range(PART_2_ENHANCEMENTS - PART_1_ENHANCEMENTS):
        infinite_pixel = enhancement_algo[0] if i % 2 == 1 else '.'
        min_coord = (min_coord[0]-2, min_coord[1]-2)
        max_coord = (max_coord[0]+2, max_coord[1]+2)
        pixels = enhance_grid(pixels, enhancement_algo, min_coord, max_coord)

    result = sum([1 if pixel == '#' else 0 for pixel in pixels.values()])
    print(f"Part 2: {result} (took {(time.time() - start_time)}s)")